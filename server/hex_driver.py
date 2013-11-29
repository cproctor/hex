import serial
import time
import logging

class HexCommunicationError(Exception):
    pass

class HexTimeoutError(Exception):
    pass

class InvalidFrameError(Exception):
    pass

class HexDriver(object):

    packet_size = 60
    GO_ON = "GO ON"
    ERROR = "ERROR"
    OK_FRAME = "OK FRAME"
    RESET = "RESET"
    READY = "READY"
    timeout = 5
    init_timeout = 1
    timedelay = 0.0001
    read_delay = 0.001

    # On Chris's laptop, the serial port is '/dev/tty.usbmodem1421'
    def __init__(self, port='/dev/tty.usbmodem1421', baud=115200, timeout=2, log=None):
        self.log = log or logging
        self.reset_timer()
        self.sio = serial.Serial(port, baud, timeout=timeout)
        self.get_response([self.READY])

    def play_animation(self, frames, loop=False, framerate=24, resetTimer=True):
        if resetTimer:
            self.reset_timer()
        for frame in frames:
            self.validate_frame(frame)
        while True:
            animationStartTime = time.time()
            for frameNum, frame in enumerate(frames):
                while time.time() - animationStartTime < (1.0/framerate) * frameNum:
                    time.sleep(self.timedelay)
                self.send_frame(frame, resetTimer=False)
            if not loop:
                break
        

    def send_frame(self, frame, resetTimer=True):
        if resetTimer:
            self.reset_timer()
        self.validate_frame(frame)
        packets = self.generate_packets(frame)
        self.send_frame_packets(packets)

    def send_frame_packets(self, packets):
        try:
            for packet in packets:
                self.serial_write(packet)        
                response = self.get_response([self.GO_ON, self.ERROR, self.OK_FRAME])
        except HexCommunicationError:
            self.log.warn("COMMUNICATION ERROR; TRYING AGAIN TO SEND FRAME")
            self.send_reset()
            self.send_frame_packets(frame)

    def send_reset(self, resetTimer=True):
        if resetTimer: 
            self.reset_timer()
        self.serial_write('R')
        self.get_response([self.RESET])

    def get_response(self, valid_responses, errMsg="Timed out"):
        time.sleep(self.read_delay)
        startResponseTime = time.time()
        while time.time() - startResponseTime < self.timeout:
            message = self.sio.readline()
            self.log.info("(%.4f) -> %s" % (self.read_timer(), message.strip('\n')))
            for vr in valid_responses:
                if message.startswith(vr):
                    return message
        raise HexConnectionError(errMsg)

    def generate_packets(self, frame): 
        frameString = 'F' + frame.__repr__().replace(' ', '')
        packetIncrements = range(0, len(frameString), self.packet_size)
        return [frameString[i:i+self.packet_size] for i in packetIncrements] 

    def validate_frame(self, frame):
        try:
            assert isinstance(frame, list)
            for layer in frame: 
                assert isinstance(layer, list)
                assert len(layer) == 2
                colors, bulbs = layer
                assert len(colors) == 4
                for color in colors:
                    assert isinstance(color, int)
                for bulb in bulbs:
                    assert isinstance(bulb, int)
        except:
            raise InvalidFrameError("%s is not a valid frame." % frame)

    def reset_timer(self):
        self.log.info("TIMER RESET")
        self.startTime = time.time()

    def read_timer(self):
        return time.time() - self.startTime

    def serial_write(self, message):
        self.log.info("(%.4f) <- %s" % (self.read_timer(), message))
        self.sio.write(message)

if __name__ == '__main__':
    background = [0,0,15,50]
    chase = [[[background, [(i) % 18]], [[5,5,10,75],[(i+1) % 18]], [[10,10,5,90], [(i+2) % 18]], [[15,15,0,100], [(i+3) % 18]]] for i in range(18)]
    hd = HexDriver(log=logging.getLogger(__name__))
    hd.send_frame([[background,range(37)]])
    hd.play_animation(chase, loop=True, resetTimer=False)
