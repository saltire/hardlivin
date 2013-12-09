import csv
import os
import re

from PIL import Image


SQSIZE = 12
files = {'marcus-squares': (0, 0, 0, 0),
         'zen-squares': (1, 1, 1, 1),
         }

outpath = os.path.join('static', 'images')
if not os.path.exists(outpath):
    os.makedirs(outpath)

for filename in os.listdir(outpath):
    os.unlink(os.path.join(outpath, filename))


for imgfile, padding in files.iteritems():
    # get square names and info
    with open(imgfile + '.csv', 'rb') as csvfile:
        sqnames = {(sx, sy): re.sub('[^\w-]', '', square.split('\n', 1)[0].lower())
                   for sy, row in enumerate(csv.reader(csvfile))
                   for sx, square in enumerate(row) if square}

    # slice image into individual squares
    img = Image.open(imgfile + '.png')
    width, height = img.size
    pt, pr, pb, pl = padding
    pwidth, pheight = SQSIZE + pl + pr, SQSIZE + pt + pb
    for sy in range(height / pwidth):
        for sx in range(width / pheight):
            if (sx, sy) in sqnames:
                # crop image and save
                px, py = sx * pwidth + pl, sy * pheight + pt
                square = img.crop((px, py, px + SQSIZE, py + SQSIZE))
                square.save(os.path.join(outpath, sqnames[sx, sy] + '.png'))
