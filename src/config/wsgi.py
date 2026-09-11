import os
import sys
from pathlib import Path

# /var/task/src
SRC_DIR = Path(__file__).resolve().parent.parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()