import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Calculate the root folder path (where manage.py lives)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Force Python to look directly inside the project root for modules
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# force Python to look directly inside 'src' for cleaner sub-app mappings
SRC_DIR = BASE_DIR / 'src'
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.config.settings.prod')

application = get_wsgi_application()

app = application
