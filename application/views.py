from flask import render_template, flash, url_for, redirect, request, abort
from jinja2 import FileSystemLoader

from application import app

import os

def reverse_url(site_nickname):
    """Construct the function that returns reverse URLs."""
    return lambda url_name: app.config["REVERSE_URLS"][site_nickname][url_name]

def get_site_nickname():
    """Get the site's nickname from the domain."""
    # Get the domain name and site nickname from the config.
    domain = request.host.split(":")[0]
    site_nickname = app.config["SITE_CONFIGURATION"].get(domain, None)
    return site_nickname

def page_handler(path):
    # Normalise the path.
    if not path.endswith("/"):
        return redirect(path + "/")
    elif not path.startswith("/"):
        path = "/" + path

    site_nickname = get_site_nickname()
    if site_nickname is None:
        abort(404)

    try:
        template_name = app.config["URLS"][site_nickname][path][0]
    except KeyError:
        abort(404)

    # Change the template loading directory.
    template_directory = os.path.join(app.root_path, "templates/", site_nickname)
    app.jinja_loader = FileSystemLoader(template_directory)
    media_url = "/media/%s/" % site_nickname
    return render_template(template_name, **{"MEDIA_URL": media_url, "url": reverse_url(site_nickname), "debug": app.config.get("DEBUG", False)})

def index_handler():
    # Flask can't handle the root URL with a path rule.
    return page_handler("/")

def warmup():
    return ''


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    site_nickname = get_site_nickname()
    if site_nickname is None:
        site_nickname = ""
    template_directory = os.path.join(app.root_path, "templates/", site_nickname)
    app.jinja_loader = FileSystemLoader(template_directory)
    media_url = "/media/%s/" % site_nickname
    return render_template('404.html', **{"MEDIA_URL": media_url, "url": reverse_url(site_nickname), "debug": app.config.get("DEBUG", False)}), 404

# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

