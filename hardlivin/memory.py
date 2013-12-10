from flask import render_template

from . import app
import csvdata


@app.route('/memory')
def memory_game():
    info, _ = csvdata.read_info()
    return render_template('memory.html', squares=info.keys())
