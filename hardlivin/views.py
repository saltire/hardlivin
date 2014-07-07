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


def get_unsold_squares(info):
    return OrderedDict((filename, sqinfo) for filename, sqinfo in info.iteritems()
                       if sqinfo['sold'] != '1')


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
@app.route('/catalogue/<sort>')
@app.route('/catalogue/<sort>/<venue>')
def catalogue(venue=None, sort=None):
    venues = {'hashtag': [('Gallery', 1, 100)],
              'snakes': [('West Wall', 0, 21), ('East Wall', 21, 63)]
              }
    if venue not in venues:
        venue = 'snakes'

    sorts = {'title': lambda sq: sq['title'],
             'position': lambda sq: (sq['column'], sq['row'])
             }
    if sort not in sorts:
        sort = 'position'

    data = CSVData()
    info = get_snakes_squares(data.info) if venue == 'snakes' else data.info
    cname, rname = ('scolumn', 'srow') if venue == 'snakes' else ('column', 'row')

    used = []
    unused = []
    sold = []
    blank = OrderedDict(((col, row), '{0} {1}{2}'.format(wall[0], col + 1 - wall[1], 'ABCDE'[row]))
                        for wall in venues[venue]
                        for col in range(wall[1], wall[2]) for row in range(5))

    for filename, sqinfo in info.iteritems():
        if sqinfo['sold'] != '1':
            if sqinfo[cname] != '' and sqinfo[rname] != '':
                col, row = int(sqinfo[cname]), int(sqinfo[rname])
                used.append({'filename': filename,
                             'title': sqinfo['title'],
                             'pos': blank.pop((col, row)),
                             'column': col,
                             'row': row,
                             })
            else:
                unused.append({'filename': filename,
                               'title': sqinfo['title'],
                               })
        else:
            sold.append({'filename': filename,
                         'title': sqinfo['title']
                         })

    return render_template('catalogue.html',
                           blank=blank,
                           used=sorted(used, key=sorts[sort]),
                           unused=sorted(unused, key=sorts['title']),
                           sold=sorted(sold, key=sorts['title']))
