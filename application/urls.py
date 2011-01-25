from flask import render_template, request
from jinja2 import FileSystemLoader

from application import app
from application import views

import os


## URL dispatch rules
# App Engine warm up handler
# See http://code.google.com/appengine/docs/python/config/appconfig.html#Warming_Requests
app.add_url_rule('/_ah/warmup', 'warmup', view_func=views.warmup)

# Home page
app.add_url_rule('/', 'index_handler', view_func=views.index_handler)
app.add_url_rule('/<path:path>', 'page_handler', view_func=views.page_handler)


