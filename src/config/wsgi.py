import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Calculate the path to the root folder (where manage.py sits)
# and ensure it's in Python's lookup registry
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

application = get_wsgi_application()

# Hook for Vercel's wrapper interface
app = application
