import os
import sys
from django.core.management import execute_from_command_line


# Define default host and port
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = "9001"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")
    sys.argv = ["manage.py", "runserver", f"{DEFAULT_HOST}:{DEFAULT_PORT}"]
    execute_from_command_line(sys.argv)
