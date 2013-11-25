import csv
import os
import re

from PIL import Image


SQSIZE = 12
SQPADDING = 1, 1, 1, 1


# get square names and info
with open('squares.csv', 'rb') as csvfile:
    sqnames = {(sx, sy): re.sub('[^\w-]', '', square.split('\n', 1)[0].lower())
               for sy, row in enumerate(csv.reader(csvfile))
               for sx, square in enumerate(row) if square}


imgpath = os.path.join('static', 'images')
if not os.path.exists(imgpath):
    os.makedirs(imgpath)

# slice image into individual squares
img = Image.open('squares.png')
width, height = img.size
pt, pr, pb, pl = SQPADDING
pwidth, pheight = SQSIZE + pl + pr, SQSIZE + pt + pb
for sy in range(height / pwidth):
    for sx in range(width / pheight):
        if (sx, sy) in sqnames:
            px, py = sx * pwidth + pl, sy * pheight + pt
            square = img.crop((px, py, px + SQSIZE, py + SQSIZE))
            square.save(os.path.join(imgpath, sqnames[sx, sy] + '.png'))
