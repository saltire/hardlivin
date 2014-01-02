from collections import OrderedDict as odict
import csv
import os
import re


DATADIR = os.path.join(os.path.dirname(__file__), 'data')


def get_filename(name):
    # convert a square name deterministically into a filename
    return re.sub('[^\w-]', '', name.lower())


def read_sourcemaps():
    """Sourcemaps is a dict indexed by source CSV filename.
    Each entry is a list of rows of square filenames,
    positioned according to the corresponding source image."""
    files = os.listdir(DATADIR)
    csvnames = [f for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

    sourcemaps = {}
    for csvname in csvnames:
        with open(os.path.join(DATADIR, csvname), 'rb') as csvfile:
            sourcemaps[csvname] = [[square for square in row] for row in csv.reader(csvfile)]
    return sourcemaps


def read_info():
    """Info is a dict indexed by square filename, ordered by appearance in the sourcemap,
    containing tuples of square name, description, and other details."""
    with open(os.path.join(DATADIR, 'info.csv'), 'rb') as csvfile:
        infofile = {row[0]: tuple(row[1:]) for row in csv.reader(csvfile)}

    # FIXME: this should really not be calling get_filename twice.
    # instead, the info file should be indexed by name, not by filename.
    return odict((get_filename(name), infofile.get(get_filename(name), (name, '')))
                 for sourcemap in read_sourcemaps().itervalues() for row in sourcemap
                 for name in row if name)


def write_info(newinfo):
    info = read_info()

    for filename, newinf in newinfo.iteritems():
        # replace stored square info with new info
        info[filename] = newinf['name'], newinf['desc']

    # write NEW info file
    with open(os.path.join(DATADIR, 'info.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for filename, fileinfo in info.iteritems():
            writer.writerow([filename] + list(fileinfo))


def read_board():
    """Board CSV contains human-readable square names,
    but return a list of rows of filenames."""
    # FIXME: this really shouldn't be calling read_info.
    # instead, this whole thing should be a class and info should be a class property.
    info = read_info()
    with open(os.path.join(DATADIR, 'board.csv'), 'rb') as csvfile:
        # FIXME: also, get_filename shouldn't be called twice - index info by name instead.
        return [[get_filename(name) if get_filename(name) in info else None for name in row]
                for row in csv.reader(csvfile)]


def write_board(rows):
    info = read_info()

    # TODO: set line delimiter to \n (here and in slice.py)
    with open(os.path.join(DATADIR, 'board.csv'), 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([info.get(filename, [''])[0] for filename in row])
