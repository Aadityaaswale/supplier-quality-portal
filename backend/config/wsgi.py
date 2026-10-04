"""
WSGI config for supplier_portal project.
Author: AADITYA ASWALE (23102B0044)
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
