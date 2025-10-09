import io
from django.core.files.storage import Storage
from django.conf import settings
from supabase import create_client, Client

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        self.bucket_name = settings.SUPABASE_BUCKET_NAME

    def _save(self, name, content):
        # Read file into bytes
        file_data = content.read()
        res = self.supabase.storage.from_(self.bucket_name).upload(name, file_data)
        if res.get("error"):
            raise Exception(res["error"]["message"])
        return name

    def exists(self, name):
        try:
            self.supabase.storage.from_(self.bucket_name).list(path=name)
            return False
        except Exception:
            return False

    def url(self, name):
        # Generate public URL (if bucket is public)
        return self.supabase.storage.from_(self.bucket_name).get_public_url(name)
