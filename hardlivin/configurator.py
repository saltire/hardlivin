from flask import jsonify, render_template, request

from . import app
import csvdata


ROWCOUNT = 5


@app.route('/')
def draw_board():
    info = csvdata.read_info()
    board = csvdata.read_board()

    unused = info.keys()
    for row in board:
        for filename in row:
            if filename:
                unused.remove(filename)

    return render_template('configurator.html', columns=zip(*board), info=info, unused=unused)


@app.route('/save', methods=['post'])
def save_changes():
    data = request.get_json()

    # save new info to squares.csv
    if data['info']:
        csvdata.write_info(data['info'])

    # save rows to board csv
    csvdata.write_board(zip(*[column.split(',') for column in data['columns']]))

    return jsonify({'saved': True})
