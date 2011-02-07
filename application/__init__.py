"""
Initialize Flask app

"""

from flask import Flask

app = Flask('application')
app.config.from_object('application.settings')

# Prevent jinja from caching templates to work around a bug.
app.jinja_env.cache = None

import urls
