from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'
    label = 'products'

    def ready(self):
        from django.db.utils import OperationalError
        from django.db import ProgrammingError

        from apps.products.seed_categories import seed_categories
        import apps.products.signals

        try:
            seed_categories()
        except (OperationalError, ProgrammingError):
            pass