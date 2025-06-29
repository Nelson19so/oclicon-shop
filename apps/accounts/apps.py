from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    label = 'accounts'  # Important for Django to identify this as 'accounts'

    def ready(self):
        import apps.accounts.signals
