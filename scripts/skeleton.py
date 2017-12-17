#!/usr/bin/env python
"""Skeleton CLI script with Django environment loaded.
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# TODO: Use relative path
PROJECT_PATH = "/Users/raul/Projects/vtalks/vtalks.net/web/"

def main():
    """Main entry point.
    """

if __name__ == '__main__':
    # Setup django environment & application.
    sys.path.append(PROJECT_PATH)
    os.chdir(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
    get_wsgi_application()

    main()
