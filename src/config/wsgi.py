import os
import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent

print("========== VERCEL DEBUG ==========")
print("SRC_DIR:", SRC_DIR)
print("SRC_DIR EXISTS:", SRC_DIR.exists())
print("APPS EXISTS:", (SRC_DIR / "apps").exists())
print("PUBLIC EXISTS:", (SRC_DIR / "apps" / "public").exists())
print("PUBLIC INIT EXISTS:", (SRC_DIR / "apps" / "public" / "__init__.py").exists())
print("SYS PATH BEFORE:", sys.path)

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

print("SYS PATH AFTER:", sys.path)

try:
    import apps
    print("IMPORT apps: SUCCESS")
except Exception as e:
    print("IMPORT apps: FAILED:", repr(e))

try:
    import apps.public
    print("IMPORT apps.public: SUCCESS")
except Exception as e:
    print("IMPORT apps.public: FAILED:", repr(e))

print("==================================")

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "src.config.settings.prod"
)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()