import os
import random

from PIL import Image

from arduino import Arduino


class ImageServer:
    def __init__(self, port='COM7'):
        imgdir = 'images'
        self.images = [os.path.join(imgdir, fname) for fname in os.listdir(imgdir)]
        self.arduino = Arduino(port, 9600)


    def run(self):
        while True:
            code = self.arduino.serial.read(1)
            if code == 'A':
                print 'got send_image code'
                self.send_image(random.choice(self.images))


    def send_image(self, imgpath):
        img = Image.open(imgpath)
        print 'sending {0}...'.format(os.path.basename(imgpath))

        odd = True
        for r, g, b, a in img.getdata():
            colour = (r >> 4, g >> 4, b >> 4) if a else (0, 0, 0)

            if odd:
                r1, g1, b1 = colour
            else:
                r2, g2, b2 = colour
                self.arduino.write_ints(r1 << 4 | g1, b1 << 4 | r2, g2 << 4 | b2)
                self.arduino.serial.read(1)

            odd = not odd

        print 'done.'


if __name__ == '__main__':
    server = ImageServer()
    server.run()
