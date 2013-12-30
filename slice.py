import csv
import os
import re
import shutil

from PIL import Image


SQSIZE = 12

sizes = [64, 128]
files = {'marcus-squares': (0, 0, 0, 0),
         'zen-squares': (1, 1, 1, 1),
         }

outpath = os.path.join('hardlivin', 'static', 'images')
if os.path.exists(outpath):
    shutil.rmtree(outpath)

for size in sizes:
    sizepath = os.path.join(outpath, str(size))
    if not os.path.exists(sizepath):
        os.makedirs(sizepath)


datapath = os.path.join('hardlivin', 'data')
for imgfile, padding in files.iteritems():
    # get square names and info
    with open(os.path.join(datapath, imgfile + '.csv'), 'rb') as csvfile:
        sqnames = {(sx, sy): re.sub('[^\w-]', '', square.lower())
                   for sy, row in enumerate(csv.reader(csvfile))
                   for sx, square in enumerate(row) if square}

    # slice image into individual squares
    for size in sizes:
        img = Image.open(os.path.join(datapath, imgfile + '.png'))
        width, height = img.size
        pt, pr, pb, pl = padding
        pwidth, pheight = SQSIZE + pl + pr, SQSIZE + pt + pb
        for sy in range(height / pwidth):
            for sx in range(width / pheight):
                if (sx, sy) in sqnames:
                    # crop image and save
                    px, py = sx * pwidth + pl, sy * pheight + pt
                    square = img.crop((px, py, px + SQSIZE, py + SQSIZE)).resize((size, size))
                    square.save(os.path.join(outpath, str(size), sqnames[sx, sy] + '.png'))
