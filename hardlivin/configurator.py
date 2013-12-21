import itertools

from flask import jsonify, render_template, request

from . import app
import csvdata


ROWCOUNT = 5


@app.route('/configurator')
def draw_board():
    info = csvdata.read_info()
    board = csvdata.read_board()

    used = list(itertools.chain(*board))
    unused = [filename for filename in info.iterkeys() if filename not in used]

    return render_template('configurator.html', columns=zip(*board), info=info, unused=unused)


@app.route('/configurator/save', methods=['post'])
def save_changes():
    data = request.get_json()

    # save new info to squares.csv
    if data['info']:
        csvdata.write_info(data['info'])

    # save rows to board csv
    csvdata.write_board(zip(*[column.split(',') for column in data['columns']]))

    return jsonify({'saved': True})
