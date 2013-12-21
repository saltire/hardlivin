from flask import render_template

from . import app


@app.route('/')
def title():
    return render_template('title.html')
