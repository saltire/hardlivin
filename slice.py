import csv
import os
import shutil

from PIL import Image


IMGPATH = os.path.join(os.path.dirname(__file__), 'hardlivin', 'static', 'images')
DATAPATH = os.path.join(os.path.dirname(__file__), 'hardlivin', 'data')
SQSIZE = 12

sizes = [144]
files = {'catalogue': (1, 1, 1, 1),
         }

print 'removing image folder...'
if os.path.exists(IMGPATH):
    shutil.rmtree(IMGPATH)

print 'creating image folders for sizes', sizes
for size in sizes:
    sizepath = os.path.join(IMGPATH, str(size))
    if not os.path.exists(sizepath):
        os.makedirs(sizepath)

titles = {}

for imgfile, padding in files.items():
    # get square names and info
    with open(os.path.join(DATAPATH, imgfile + '.csv'), 'rb') as csvfile:
        squares = set((sx, sy) for sy, row in enumerate(csv.reader(csvfile))
                      for sx, title in enumerate(row) if title)
    with open(os.path.join(DATAPATH, imgfile + '.csv'), 'rb') as csvfile:
        titles.update({title: '{0}-{1}-{2}'.format(imgfile, sx, sy)
                       for sy, row in enumerate(csv.reader(csvfile))
                       for sx, title in enumerate(row) if title})
        print 'read {0} squares from {1}, cropping and saving...'.format(len(squares), imgfile)

    # slice image into individual squares
    for size in sizes:
        img = Image.open(os.path.join(DATAPATH, imgfile + '.png'))
        width, height = img.size
        pt, pr, pb, pl = padding
        pwidth, pheight = SQSIZE + pl + pr, SQSIZE + pt + pb
        for sx, sy in squares:
            # crop image and save
            px, py = sx * pwidth + pl, sy * pheight + pt
            square = img.crop((px, py, px + SQSIZE, py + SQSIZE)).resize((size, size))
            square.save(os.path.join(IMGPATH, str(size),
                                     '{0}-{1}-{2}.png'.format(imgfile, sx, sy)))
