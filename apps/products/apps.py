from django.apps import AppConfig

class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.products'

    # this function runs the apps/product/seed_categories when ever the app runs 
    def ready(self):
        import apps.products.signals
