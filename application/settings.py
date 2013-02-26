"""
settings.py

Configuration for Flask app

Important: Place your keys in the secret_keys.py module, 
           which should be kept out of version control.

"""

import os

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY

# Add the domains and site aliases. Multiple domains can map to a single alias.
SITE_CONFIGURATION = {
    "www.example.com": "example",
    "test.example.com": "example",
}

URLS = {}

# Define the URL mappings from URLs to templates for each alias, and their
# names for referencing reverse URLs.
URLS["example"] = {
    "/": ("index.html", "index"),
    "/test/": ("test.html", "test"),
}

# Reverse the URLs into (name, url) pairs.
REVERSE_URLS = dict((domain, dict((value[1], key) for (key, value) in URLS[domain].items())) for domain in URLS.keys()) 

DEBUG_MODE = False

# Auto-set debug mode based on App Engine dev environ
if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    DEBUG_MODE = True

DEBUG = DEBUG_MODE

# Set secret keys for CSRF protection
SECRET_KEY = CSRF_SECRET_KEY
CSRF_SESSION_LKEY = SESSION_KEY

CSRF_ENABLED = True
