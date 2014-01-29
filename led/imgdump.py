import os

from PIL import Image

from imgserver import pack_colours


for fname in os.listdir('images'):
    packed = pack_colours(Image.open('images/' + fname).getdata())
    for row in zip(*[iter(packed)] * 18):
        print '   ', ','.join('{0:#04X}'.format(b) for b in row)
    break
