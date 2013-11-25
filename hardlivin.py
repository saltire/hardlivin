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
    filename = re.sub('[^\w-]', '', name.lower())
    return filename, name, desc


@app.before_request
def load_csvs():
    # abort if request is for a static file
    if '/static/' in request.path:
        return

    # squares.csv contains name and description separated by a line break
    # g.squares is an ordered dict >> filename: name, description
    # filenames are generated from the name
    g.squares = OrderedDict()
    with open('squares.csv', 'rb') as csvfile:
        for row in csv.reader(csvfile):
            for square in row:
                if square:
                    filename, name, desc = get_square_info(square)
                    g.squares[filename] = name, desc

    # board.csv contains name
    # g.board is a dict >> (x, y): filename
    g.board = {}
    with open('board.csv', 'rb') as csvfile:
        for y, row in enumerate(csv.reader(csvfile)):
            for x, square in enumerate(row):
                if square:
                    filename, name, desc = get_square_info(square)
                    if filename in g.squares:
                        g.board[x, y] = filename


@app.route('/')
def draw_board():
    unused = g.squares.keys()
    for filename in g.board.itervalues():
        unused.remove(filename)

    colcount = max(xx for xx, _ in g.board.iterkeys()) + 1
    columns = [[(g.board[x, y] if (x, y) in g.board else None)
                for y in range(ROWCOUNT)]
               for x in range(colcount)]

    return render_template('squares.html', columns=columns, squares=g.squares, unused=unused)


@app.route('/save', methods=['post'])
def save_board():
    rows = zip(*[column.split(',') for column in request.form.getlist('columns[]')])

    with open('board.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        for row in rows:
            writer.writerow([(g.squares[filename][0] if filename in g.squares else '')
                             for filename in row])

    return jsonify({'saved': True})


if __name__ == '__main__':
    app.debug = True
    app.run()
