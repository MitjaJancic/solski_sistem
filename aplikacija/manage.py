#!/usr/bin/env python
"""Django manage.py"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "solski_sistem.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django ni nameščen ali ni dosegljiv v virtualnem okolju."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
