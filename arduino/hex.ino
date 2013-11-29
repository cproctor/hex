#include <G35String.h>

#define LIGHT_COUNT (38)
#define G35_PIN (13)
#define CHANNEL_MAX (0xF)
#define FRAME_START_CHAR ('F')
#define RESET_CHAR ('R')
#define SET_DELAY_CHAR ('D')
#define ASCII_DIGIT_OFFSET (48)

G35String lights(G35_PIN, LIGHT_COUNT);
int maxima[] = {
  CHANNEL_MAX,
  CHANNEL_MAX,
  CHANNEL_MAX,
  G35::MAX_INTENSITY
};
int delayTime = 100;
boolean inError = false;
boolean waiting = false;

// These three safe methods are currently blocking. That will be
// a problem when we're trying to run animations, if we want to 
// cache frames on the Arduino. Let's cross that bridge when we come
// to it. If the serial communication is fast enough, we can just 
// send the frames when they're needed.
int safePeek() {
  if (Serial.available() > 0) {
    waiting = false;
    return Serial.peek();
  } else {
    if (!waiting) {
      waiting = true;
      Serial.println("GO ON");
    }
    delay(delayTime);
    return safePeek();
  }
}

int safeRead() {
  if (Serial.available() > 0) {
    waiting = false;
    return Serial.read();
  } else {
    if (!waiting) {
      waiting = true;
      Serial.println("GO ON");
    }
    delay(delayTime);
    return safeRead();
  }
}

// Only handles ints up to 999. That's enough for me!
int safeParseInt() {
  int digits[] = {-1,-1,-1};
  int value = 0;
  for (int i = 0; i < 3; i = i+1) {
    if (isDigit(safePeek())) {
      digits[i] = safeRead() - ASCII_DIGIT_OFFSET;
      //Serial.println(digits[i]);
    } 
  }
  for (int i = 0; i < 3; i = i+1) {
    if (digits[i] == -1) {
      return value; 
    }
    if (value == 0) {
       value = digits[i];
    } else {
       value = value * 10 + digits[i];
    }
  }
  return value;
}

boolean isControlChar(int c) {
  return (
    c == '[' || 
    c == ']' || 
    c == ',' || 
    c == FRAME_START_CHAR || 
    c == RESET_CHAR ||
    c == SET_DELAY_CHAR
  );
}

// Skip characters that don't matter.
// If the next character is the reset char, consume it and return 
// false. Client functions are responsible for propogating this 
// message to their parents. Thus, advance should be used like this:
// if (!advance()) { return false; }
boolean advance() {
  int n = safePeek();
  while (!(isDigit(n) || isControlChar(n))) {
    safeRead();
    n = safePeek();
  }
  if (n == RESET_CHAR || n == FRAME_START_CHAR) {
    safeRead();
    return false;
  } else {
    return true;
  }
}

//
// Parse two or three numbers from the stream.
// If we return false, this means the frame should
// stop.
boolean read_frame_layer() {
  //Serial.println("Starting to read a layer...");
  int colors[4];                                    // colors[3] is intensity
  if (!advance())                 { return false; }
  if (safeRead() != '[')       { return false; } // Opening bracket for layer
  if (!advance())                 { return false; }
  if (safeRead() != '[')       { return false; } // Opening bracket for colors
  
  for (int i = 0; i < 4; i = i+1) {     // Read colors (and intensity)
    if (!advance())               { return false; }
    if (!isDigit(safePeek()))  { return false; }
    //colors[i] = constrain(safeParseInt(), 0, maxima[i]);
    colors[i] = safeParseInt();
    if (!advance())               { return false; }
    if (safePeek() == ',') {
      safeRead();
    }
  }
  
  if (!advance())                 { return false; } 
  if (safeRead() != ']')       { return false; } // Closing bracket for colors
  if (!advance())                 { return false; } 
  if (safeRead() != ',')       { return false; } // Separates colors from bulbs
  if (!advance())                 { return false; }
  if (safeRead() != '[')       { return false; } // Opening bracket for bulbs
  
  if (!advance())                 { return false; }
  while (isDigit(safePeek())) {                  // Read bulb numbers
    int bulbNum = safeParseInt();
    Serial.print("OK BULB  ");
    Serial.print(bulbNum);
    Serial.print(": (");
    for (int i = 0; i < 4; i = i+1) { Serial.print(colors[i]); if (i < 3) {Serial.print(',');} }
    Serial.println(')');
    lights.set_color_if_in_range(bulbNum, colors[3], COLOR(colors[0], colors[1], colors[2]));
    if (!advance())               { return false; } 
    if (safePeek() == ',') {                    
      safeRead();
      if (!advance())             { return false; }
    } 
  }
  
  if (safeRead() != ']')       { return false; } // Closing bracket for bulbs
  if (!advance())                 { return false; } 
  if (safeRead() != ']')       { return false; } // Closing bracket for layer
  return true;
}

// A frame is composed of frame layers. Read the opening bracket
boolean read_frame() {
  //Serial.println("Starting to read a frame..."); 
  if (safeRead() != FRAME_START_CHAR) { return false; }
  if (!advance())                 { return false; }
  if (safeRead() != '[')       { return false; } // Opening bracket for layers
  while (true) {
    boolean success = read_frame_layer();
    if (!success)                 { return false; }
    Serial.println("OK LAYER");
    
    if (!advance())               { return false; }
    if (safePeek() == ',') {
      safeRead();
      if (!advance())             { return false; }
    } else {
      break;
    }
  }
  if (safeRead() != ']')       { return false; } // Closing bracket for bulbs
  return true;
}

void setup() {
  Serial.begin(9600);
  lights.enumerate();
  Serial.println("READY");
}

void loop() {
  if (Serial.available() > 0) {
    delay(delayTime);
    while (Serial.available() > 0) {
      int mode = Serial.peek();
      if (mode == FRAME_START_CHAR) {
        inError = false;
        boolean success = read_frame();
        if (success) {
          Serial.println("OK FRAME");
        } else {
          Serial.println("RESET");  
        }
      } else if (mode == SET_DELAY_CHAR) {
        inError = false;
        delayTime = Serial.parseInt();
        Serial.print("OK DELAY IS ");
        Serial.println(delayTime);
      } else if (mode == RESET_CHAR) {
        inError = false;
        Serial.read();
        Serial.println("RESET");
      } else { // Don't care.
        if (!inError) {
          inError = true;
          Serial.print("ERROR: ");
        }
        int nextChar = Serial.read();
        if (Serial.available() == 0) {
          inError = false;
          Serial.println(char(nextChar));
        } else {
          Serial.print(char(nextChar));
        }
      }
    }
  }
}


