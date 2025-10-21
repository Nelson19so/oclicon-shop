import os
import requests
from django.core.files.storage import Storage

BYTESCALE_API_KEY = os.getenv("BYTESCALE_API_KEY")
ACCOUNT_ID = os.getenv("BYTESCALE_ACCOUNT_ID")

class BytescaleStorage(Storage):
    def _save(self, name, content):
        """Upload file to Bytescale via REST API"""
        upload_url = f"https://api.bytescale.com/v2/accounts/{ACCOUNT_ID}/uploads/form_data"
        headers = {"Authorization": f"Bearer {BYTESCALE_API_KEY}"}

        # Remove slashes or path parts (Bytescale forbids '/')
        file_name = os.path.basename(name)

        files = {"file": (file_name, content.read())}

        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()

        data = response.json()
        return data["filePath"]  # e.g. "/k12345/filename.png"

    def url(self, name):
        """Return the full CDN URL"""
        if name.startswith("http"):
            return name
        return f"https://upcdn.io{str(name)}"
