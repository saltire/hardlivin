from collections import OrderedDict
import csv
import re

from flask import Flask, g, jsonify, render_template, request


app = Flask(__name__)
app.secret_key = '}\xf6\x92\xa8a\x82\xd9\x03aXL^/a}A\xd0zt1\x9c4\x81\x15'
app.jinja_options = dict(app.jinja_options, trim_blocks=True, lstrip_blocks=True)

ROWCOUNT = 5


def get_square_info(square):
    try:
        name, desc = square.split('\n', 1)
    except ValueError:
        name, desc = square, ''

    # generate filename from name
    filename = re.sub('[^\w-]', '', name.lower())
    return filename, (name, desc)


def get_filename(square):
    if not square:
        return None
    filename = get_square_info(square)[0]
    return filename if filename in g.info else None


@app.before_request
def load_csvs():
    # abort if request is for a static file
    if '/static/' in request.path:
        return

    # g.info is an ordered dict: {filename: name, description}
    # g.sourcemap is a list of rows containing filenames, in source image position
    g.info = OrderedDict()
    g.sourcemap = []
    with open('squares.csv', 'rb') as csvfile:
        for row in csv.reader(csvfile):
            g.info.update(get_square_info(square) for square in row if square)
            g.sourcemap.append([get_filename(square) for square in row])

    # g.board is a list of rows containing filenames, in board position
    with open('board.csv', 'rb') as csvfile:
        g.board = [[get_filename(square) for square in row] for row in csv.reader(csvfile)]


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
    print data['info']
    if data['info']:
        for filename, info in data['info'].iteritems():
            g.info[filename] = info['name'], info['desc']

        with open('squares.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            for row in g.sourcemap:
                writer.writerow([('\n'.join(g.info[filename]).strip() if filename in g.info else '')
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
