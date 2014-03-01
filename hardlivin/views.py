import itertools
from collections import OrderedDict

from flask import jsonify, render_template, request

from . import app
from csvdata import CSVData


VENUES = {'hashtag': 100,
          'snakes': 42,
          }


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


def get_snakes_squares(info):
    return OrderedDict((filename, sqinfo) for filename, sqinfo in info.iteritems()
                       if sqinfo['snakes'] == '1')


@app.route('/sales')
def draw_sales():
    data = CSVData()
    info = get_snakes_squares(data.info)

    colcount = VENUES['snakes']
    columns = [[''] * 5 for _ in range(colcount)]
    unused = []

    for filename, sqinfo in info.iteritems():
        co, ro = sqinfo['scolumn'], sqinfo['srow']

        if co != '' and ro != '':
            columns[colcount - int(co) - 1][int(ro)] = filename
        else:
            unused.append(filename)

    return render_template('sales.html', info=info, columns=columns, unused=unused)


@app.route('/configurator')
@app.route('/configurator/<venue>')
def draw_configurator(venue=None):
    if venue not in VENUES:
        venue = 'hashtag'

    data = CSVData()
    info = get_snakes_squares(data.info) if venue == 'snakes' else data.info

    colcount = VENUES[venue]
    columns = [[''] * 5 for _ in range(colcount)]
    unused = []

    for filename, sqinfo in info.iteritems():
        co, ro = ((sqinfo['column'], sqinfo['row']) if venue == 'hashtag'
                  else (sqinfo['scolumn'], sqinfo['srow']))

        if co != '' and ro != '':
            columns[colcount - int(co) - 1][int(ro)] = filename
        else:
            unused.append(filename)

    return render_template('configurator.html',
                           info=info, columns=columns, unused=unused, venue=venue)


@app.route('/configurator/save', methods=['post'])
def save_changes():
    data = CSVData()

    # save new info to source csvs
    data.write_info(request.get_json())

    return jsonify({'saved': True})


@app.route('/catalogue')
@app.route('/catalogue/<venue>')
@app.route('/catalogue/<venue>/<sort>')
def catalogue(venue=None, sort=None):
    if venue not in ['hashtag', 'snakes']:
        venue = 'snakes'
    if sort not in ['title', 'position']:
        sort = 'position'

    sorts = {'title': lambda sq: sq['title'],
             'position': lambda sq: (sq['column'], sq['row'])
             }

    data = CSVData()
    info = get_snakes_squares(data.info) if venue == 'snakes' else data.info
    cname, rname = ('scolumn', 'srow') if venue == 'snakes' else ('column', 'row')
    info = [{'filename': filename,
             'title': sqinfo['title'],
             'pos': '{0}{1}'.format(int(sqinfo[cname]) + 1, 'ABCDE'[int(sqinfo[rname])]),
             'column': int(sqinfo[cname]),
             'row': int(sqinfo[rname]),
             }
            for filename, sqinfo in info.iteritems()
            if sqinfo[cname] != '' and sqinfo[rname] != '']

    return render_template('catalogue.html', info=sorted(info, key=sorts[sort]))



