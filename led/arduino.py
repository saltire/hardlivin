import time

from serial import Serial


class Arduino:
    def __init__(self, port, baud):
        self.serial = Serial(port, baud)
        time.sleep(2)

    def write_ints(self, *ints):
        print 'sending bytes', [hex(i) for i in ints]
        self.serial.write(''.join(chr(i) for i in ints))
