import os

from PIL import Image

from arduino import Arduino


ard = Arduino('COM7', 9600)

for fname in os.listdir('images'):
    img = Image.open('images/{0}'.format(fname))
    print 'sending {0}...'.format(fname)

    odd = True
    for r, g, b, a in img.getdata():
        colour = (r >> 4, g >> 4, b >> 4) if a else (0, 0, 0)

        if odd:
            r1, g1, b1 = colour
        else:
            r2, g2, b2 = colour
            ard.write_ints(r1 << 4 | g1,
                           b1 << 4 | r2,
                           g2 << 4 | b2)

            ard.serial.read(1)

        odd = not odd

    print 'done.'
    break

raw_input()
