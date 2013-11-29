import serial

class FrameError(Exception):
    "For invalid frames"
    pass

class HexDriver(object):
    # On Chris's laptop, the serial port is '/dev/tty.usbmodem1421'
    def __init__(self, port='/dev/tty.usbmodem1421', baud=9600, timeout=2):
        self.sio = serial.Serial(port, baud, timeout=timeout)

    def send_frame(self, frame):
        self.sio.write(self.translate_frame(frame))
        return self.sio.readline()

    def translate_frame(self, frame):
        "Translates a frame into its string representation for tty"
        return ','.join([ str(param) for param in [
            frame['first'],
            frame['last'],
            frame['red'], 
            frame['green'], 
            frame['blue'], 
            frame['intensity']
        ]])


