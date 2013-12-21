import re

from flask import Flask


app = Flask(__name__)
app.secret_key = '}\xf6\x92\xa8a\x82\xd9\x03aXL^/a}A\xd0zt1\x9c4\x81\x15'
app.jinja_options = dict(app.jinja_options, trim_blocks=True, lstrip_blocks=True)


# view functions must be imported into this module for routing to work
import configurator
import memory
import title


def get_filename(name):
    # convert a square name deterministically into a filename
    return re.sub('[^\w-]', '', name.lower())
