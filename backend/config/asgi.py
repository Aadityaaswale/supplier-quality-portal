"""
ASGI config for supplier_portal project.
Author: AADITYA ASWALE (23102B0044)
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_asgi_application()
