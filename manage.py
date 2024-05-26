#!/usr/bin/env python
import os
import sys
from decouple import config
from pathlib import Path
import random
import string


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sokakagzi.settings')
    try:
        from django.core.management import execute_from_command_line
        from django.core.management import call_command
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Generate a new SECRET_KEY if not present in .env
    env_path = Path(__file__).resolve().parent / '.env'
    if not env_path.is_file() or not config('SECRET_KEY', default=None):
        new_secret_key = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))
        with open(env_path, 'a') as env_file:
            env_file.write(f'\nSECRET_KEY={new_secret_key}\n')

    execute_from_command_line(sys.argv)

    # Create superuser if not exists
    if 'runserver' in sys.argv:
        call_command('createsuperuser_if_not_exists')


if __name__ == '__main__':
    main()
