from django.db import migrations
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
import os

load_dotenv()

def create_superuser(apps, scheme_editor):
    User = apps.get_model("accounts", "CustomUser")

    User.objects.create(
        username=os.getenv('username'),
        email=os.getenv('email'),
        password=os.getenv('password'),
        is_staff=True,
        is_superuser=True
    )

class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.RunPython(create_superuser)
    ]