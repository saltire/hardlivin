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
            elif code == 'B':
                print 'got send_col code'
                self.send_cols(random.choice(self.images))


    def convert_colour(self, r, g, b, a):
        return (r >> 4, g >> 4, b >> 4) if a else (0, 0, 0)


    def send_image(self, imgpath):
        img = Image.open(imgpath)
        print 'sending {0}...'.format(os.path.basename(imgpath))

        # this next line breaks the list of pixels into groups of 2
        for colour1, colour2 in zip(*[iter(img.getdata())] * 2):
            r1, g1, b1 = self.convert_colour(*colour1)
            r2, g2, b2 = self.convert_colour(*colour2)

            self.arduino.write_ints(r1 << 4 | g1, b1 << 4 | r2, g2 << 4 | b2)
            self.arduino.serial.read(1)

        print 'done.'


    def send_cols(self, imgpath):
        img = Image.open(imgpath)
        pix = img.load()
        w, h = img.size
        for x in xrange(w):
            print 'sending column', x
            if x > 0:
                self.arduino.serial.read(1)
            for y in xrange(0, h, 2):
                r1, g1, b1 = self.convert_colour(*pix[x, y])
                r2, g2, b2 = self.convert_colour(*pix[x, y + 1])
                self.arduino.write_ints(r1 << 4 | g1, b1 << 4 | r2, g2 << 4 | b2)



if __name__ == '__main__':
    server = ImageServer()
    server.run()
