#!/usr/bin/env python
"""
Standalone database seeding script for the Supplier Quality Review Portal.
Student: AADITYA ASWALE (23102B0044)
"""

import os
import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent / 'backend'
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("Executing database migrations...")
    call_command('migrate')
    print("Executing portal data seeding...")
    call_command('seed_portal')
    print("Database is primed and ready!")
