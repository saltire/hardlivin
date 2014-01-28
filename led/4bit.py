import os

from PIL import Image

from arduino import Arduino


ard = Arduino('COM7', 9600)

for fname in os.listdir('images'):
    print fname
    img = Image.open('images/{0}'.format(fname))

    #out = Image.new('RGB', img.size)
    #out.putdata([(r >> 4 << 4, g >> 4 << 4, b >> 4 << 4) if a else (0, 0, 0)
    #             for r, g, b, a in img.getdata()])
    #out.save('out/{0}'.format(fname))

    odd = True
    for r, g, b, a in img.getdata():
        colour = (r >> 4, g >> 4, b >> 4) if a else (0, 0, 0)
        print (r, g, b, a), colour

        if odd:
            r1, g1, b1 = colour
        else:
            r2, g2, b2 = colour
            ard.write_ints(r1 << 4 | g1,
                           b1 << 4 | r2,
                           g2 << 4 | b2)

            print [ord(c) for c in ard.serial.read(5)]

        odd = not odd
    break

raw_input()
