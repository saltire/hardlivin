import itertools

from flask import jsonify, render_template, request

from . import app
from csvdata import CSVData


@app.route('/')
def title():
    return render_template('title.html')


@app.route('/play')
def draw_board():
    data = CSVData()
    return render_template('play.html', columns=zip(*data.board), info=data.info)


@app.route('/memory')
def memory_game():
    data = CSVData()
    return render_template('memory.html', squares=data.info.keys())


@app.route('/configurator')
def draw_configurator():
    data = CSVData()
    used = list(itertools.chain(*data.columns))
    unused = [filename for filename in data.info.iterkeys() if filename not in used]

    return render_template('configurator.html', columns=data.columns, info=data.info, unused=unused)


@app.route('/configurator/save', methods=['post'])
def save_changes():
    data = CSVData()

    # save new info to source csvs
    data.write_info(request.get_json())

    return jsonify({'saved': True})


@app.route('/catalogue')
def catalogue():
    data = CSVData()
    return render_template('catalogue.html', info=data.info)



