from collections import OrderedDict
import csv
import os
import re


DATADIR = os.path.join(os.path.dirname(__file__), 'data')


def get_filename(name):
    # convert a square name deterministically into a filename
    return re.sub('[^\w-]', '', name.lower())


def read_sourcemap():
    files = os.listdir(DATADIR)
    csvnames = [f for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

    sourcemap = {}
    for csvname in csvnames:
        with open(os.path.join(DATADIR, csvname), 'rb') as csvfile:
            sourcemap[csvname] = [[(get_filename(square) if square else None) for square in row]
                                  for row in csv.reader(csvfile)]

    return sourcemap


def read_info():
    with open(os.path.join(DATADIR, 'info.csv'), 'rb') as csvfile:
        return OrderedDict((row[0], row[1:]) for row in csv.reader(csvfile))


def write_info(newinfo):
    sourcemap = read_sourcemap()
    info = read_info()

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

    # write NEW info file
    with open(os.path.join(DATADIR, 'info.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for filename, fileinfo in info.iteritems():
            writer.writerow([filename] + list(fileinfo))


def read_board():
    # cells in board csv should contain name
    # g.board is a list of rows containing filenames, in board position
    with open(os.path.join(DATADIR, 'board.csv'), 'rb') as csvfile:
        return [[get_filename(name) for name in row] for row in csv.reader(csvfile)]


def write_board(rows):
    info = read_info()

    with open(os.path.join(DATADIR, 'board.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([info.get(filename, [''])[0] for filename in row])
