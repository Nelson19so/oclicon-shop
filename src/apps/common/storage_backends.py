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
        files = {"file": (name, content.read())}

        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()

        data = response.json()
        # ✅ Save only the path part (not full URL)
        return data["filePath"]  # e.g. "/k12345/filename.jpg"

    def url(self, name):
        """Return the full CDN URL"""
        # Ensure we always return full URL
        if name.startswith("http"):
            return name
        return f"https://upcdn.io{str(name)}"
