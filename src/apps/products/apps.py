from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.products'

    # this function runs the apps/product/seed_categories when ever the app runs 
    def ready(self):
        from django.db.utils import OperationalError
        from django.db import ProgrammingError
        from src.apps.products.seed_categories import seed_categories
        import src.apps.products.signals

        try:
            seed_categories()
        except (OperationalError, ProgrammingError):
            pass  # Happens during first migration or db unready