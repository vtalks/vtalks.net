#!/usr/bin/env python

import os
import sys
from django.core.wsgi import get_wsgi_application

# TODO: Use relative path
project_path = "/Users/raul/Projects/vtalks/vtalks.net/web/"

# This is so my local_settings.py gets loaded.
sys.path.append(project_path)
os.chdir(project_path)

# This is so Django knows where to find stuff.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

# This is so models get loaded.
application = get_wsgi_application()

# My script starts here
