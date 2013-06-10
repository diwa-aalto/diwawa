#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    # Settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diwawa.settings')

    # Import
    from django.core.management import execute_from_command_line

    # Execute
    execute_from_command_line(sys.argv)
