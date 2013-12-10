from collections import OrderedDict
import csv
import os
import re


DATADIR = os.path.join(os.path.dirname(__file__), 'data')


def get_filename(name):
    # convert a square name deterministically into a filename
    return re.sub('[^\w-]', '', name.lower())


def read_info():
    files = os.listdir(DATADIR)
    csvnames = [f for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

    # cells in info csv should contain name, then optionally a line break and a description
    # g.info is an ordered dict: {filename: name, description, csv filename}
    # g.sourcemap is a list of rows containing filenames, in source image position
    info = OrderedDict()
    sourcemap = {}
    for csvname in csvnames:
        sourcemap[csvname] = []
        with open(os.path.join(DATADIR, csvname), 'rb') as csvfile:
            for row in csv.reader(csvfile):
                sourcerow = []
                for square in row:
                    if square:
                        name, desc = square.split('\n', 1) if '\n' in square else (square, '')
                        filename = get_filename(name)
                        info[filename] = name, desc, csvname
                        sourcerow.append(filename)
                    else:
                        sourcerow.append(None)
                sourcemap[csvname].append(sourcerow)

    return info, sourcemap


def write_info(newinfo):
    info, sourcemap = read_info()

    for filename, newinf in newinfo.iteritems():
        # replace stored square info with new info
        info[filename] = newinf['name'], newinf['desc'], info[filename][2]

    # rewrite info csv file
    for csvname in sourcemap:
        with open(os.path.join(DATADIR, csvname), 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in sourcemap[csvname]:
                writer.writerow([('\n'.join(info.get(filename, [])[:2]).strip())
                                 for filename in row])


def read_board():
    # cells in board csv should contain name
    # g.board is a list of rows containing filenames, in board position
    with open(os.path.join(DATADIR, 'board.csv'), 'rb') as csvfile:
        return [[get_filename(name) for name in row] for row in csv.reader(csvfile)]


def write_board(rows):
    info, _ = read_info()

    with open(os.path.join(DATADIR, 'board.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([info.get(filename, [''])[0] for filename in row])
