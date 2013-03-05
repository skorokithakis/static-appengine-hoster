from flask import Flask, render_template, redirect, request, abort
from jinja2 import FileSystemLoader

import os

app = Flask('application')
app.config.from_object('application.settings')

# Prevent jinja from caching templates to work around a bug.
app.jinja_env.cache = None


def reverse_url(site_nickname):
    """Construct the function that returns reverse URLs."""
    def reverse(url_name):
        site = app.config["REVERSE_URLS"].get(site_nickname)
        if site is None:
            return ""
        else:
            return site.get(url_name, "")
    return reverse


@app.route('/', defaults={'path': '/'})
@app.route('/<path:path>')
def page_handler(path):
    # Normalise the path.
    if not path.endswith("/"):
        return redirect(path + "/")
    elif not path.startswith("/"):
        path = "/" + path

    # Get the domain name and site nickname from the config.
    domain = request.host.split(":")[0]
    site_nickname = app.config["SITE_CONFIGURATION"].get(domain, None)
    if site_nickname is None:
        site_nickname = domain

    template_directory = os.path.join(app.root_path, "templates/", site_nickname)

    try:
        template_name = app.config["URLS"][site_nickname][path][0]
    except KeyError:
        # Normalize the path to remove slashes from beginning and end.
        filepath = path[1:-1]
        # Add the path/index part.
        paths = [os.path.join(filepath + "index")]

        # Add the path/ part if the path isn't the root.
        if filepath:
            paths.append(filepath)

        filenames = []
        # Add .htm and .html to everything.
        for filename in paths:
            filenames.append(filename + ".htm")
            filenames.append(filename + ".html")

        for filename in filenames:
            if os.path.exists(os.path.join(template_directory, filename)):
                template_name = filename
                break
        else:
            abort(404)

    # Change the template loading directory.
    app.jinja_loader = FileSystemLoader(template_directory)
    media_url = "/media/%s/" % site_nickname
    return render_template(template_name, **{"MEDIA_URL": media_url, "url": reverse_url(site_nickname), "debug": app.config.get("DEBUG", False)})


@app.route('/', defaults={'path': ''})
@app.route('/_ah/warmup')
def warmup():
    return ''


## Error handlers
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    domain = request.host.split(":")[0]
    site_nickname = app.config["SITE_CONFIGURATION"].get(domain, None)
    if site_nickname is None:
        site_nickname = domain
    template_directory = os.path.join(app.root_path, "templates/", site_nickname)
    app.jinja_loader = FileSystemLoader(template_directory)
    media_url = "/media/%s/" % site_nickname
    return render_template('404.html', **{"MEDIA_URL": media_url, "url": reverse_url(site_nickname), "debug": app.config.get("DEBUG", False)}), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run()
