import os
import requests
from django.core.files.storage import Storage


BYTESCALE_API_KEY = os.getenv("BYTESCALE_API_KEY")
ACCOUNT_ID = os.getenv("BYTESCALE_ACCOUNT_ID")


class BytescaleStorage(Storage):
    def _save(self, name, content):
        """
        Upload file to Bytescale via REST API.
        Fixes 'Invalid path' by stripping all slashes and directories.
        """
        upload_url = f"https://api.bytescale.com/v2/accounts/{ACCOUNT_ID}/uploads/form_data"

        headers = {
            "Authorization": f"Bearer {BYTESCALE_API_KEY}",
        }

        # ✅ Remove any leading "/" and directories like "ads/"
        cleaned_name = name.lstrip("/").split("/")[-1]

        # ✅ Read file content safely
        content.open()
        files = {
            "file": (cleaned_name, content.read()),
        }

        response = requests.post(upload_url, headers=headers, files=files)
        response.raise_for_status()

        data = response.json()
        return data["fileUrl"]

    def url(self, name):
        # Django expects a URL for displaying the file
        return name
