===========
Description
===========

``static-appengine-hoster`` is a Flask application that will allow you to host
static sites on App Engine under multiple domains.

Usage
-----

To use ``static-appengine-hoster``, all you need to do is download it, install
the appropriate packages in the ``packages`` directory, add your files and
change the settings.

The required packages are:

* flask
* jinja2
* werkzeug

To add your sites, follow the example. Create directories under the
``templates`` and ``media`` directories with the name of the site you want to
host and add your files there. To reference media under your media directory
you can use the {{ MEDIA_URL }} variable in your templates, and to get the URL
for a specific page you can use the url() function.

You can optionally add your site's domains and alias in ``settings.py``, and then
you can define and name the URLs and specify the template they will be rendered
with.

Alternatively, you can just create folders called `www.yourdomain.com` for each
site you want to host, and put html templates in that folder. The folder structure
will be preserved, so, for example, the file `mydomain/test/hello.html` will be
accessible under `http://mydomain/test/hello/`.

License
-------

``static-appengine-hoster`` is distributed under the BSD license.
