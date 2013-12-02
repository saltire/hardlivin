from collections import OrderedDict
import csv
import os
import re

from flask import Flask, g, jsonify, render_template, request


app = Flask(__name__)
app.secret_key = '}\xf6\x92\xa8a\x82\xd9\x03aXL^/a}A\xd0zt1\x9c4\x81\x15'
app.jinja_options = dict(app.jinja_options, trim_blocks=True, lstrip_blocks=True)

ROWCOUNT = 5


def get_filename(name):
    # convert a square name deterministically into a filename
    return re.sub('[^\w-]', '', name.lower())


@app.before_request
def load_csvs():
    # abort if request is for a static file
    if '/static/' in request.path:
        return

    files = os.listdir('.')
    csvnames = [f for f in files if f[-4:] == '.csv' and f[:-4] + '.png' in files]

    # cells in info csv should contain name, then optionally a line break and a description
    # g.info is an ordered dict: {filename: name, description, csv filename}
    # g.sourcemap is a list of rows containing filenames, in source image position
    g.info = OrderedDict()
    g.sourcemap = {}
    for csvname in csvnames:
        g.sourcemap[csvname] = []
        with open(csvname, 'rb') as csvfile:
            for row in csv.reader(csvfile):
                sourcerow = []
                for square in row:
                    if square:
                        name, desc = square.split('\n', 1) if '\n' in square else (square, '')
                        filename = get_filename(name)
                        g.info[filename] = name, desc, csvname
                        sourcerow.append(filename)
                    else:
                        sourcerow.append(None)
                g.sourcemap[csvname].append(sourcerow)

    # cells in board csv should contain name
    # g.board is a list of rows containing filenames, in board position
    with open('board.csv', 'rb') as csvfile:
        g.board = [[get_filename(name) for name in row] for row in csv.reader(csvfile)]


@app.route('/')
def draw_board():
    unused = g.info.keys()
    for row in g.board:
        for filename in row:
            if filename:
                unused.remove(filename)

    return render_template('squares.html', columns=zip(*g.board), info=g.info, unused=unused)


@app.route('/save', methods=['post'])
def save_changes():
    data = request.get_json()

    # save info to squares.csv
    if data['info']:
        for filename, info in data['info'].iteritems():
            # replace stored square info with new info
            g.info[filename] = info['name'], info['desc'], g.info[filename][2]

        # rewrite info csv file
        for csvname in g.sourcemap:
            with open(csvname, 'wb') as csvfile:
                writer = csv.writer(csvfile)
                for row in g.sourcemap[csvname]:
                    writer.writerow([('\n'.join(g.info.get(filename, [])).strip())
                                     for filename in row])

    # save rows to board csv
    with open('board.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in zip(*[column.split(',') for column in data['columns']]):
            writer.writerow([(g.info[filename][0] if filename in g.info else '')
                             for filename in row])

    return jsonify({'saved': True})


if __name__ == '__main__':
    app.debug = True
    app.run()
