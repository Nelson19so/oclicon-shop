# apps/product/seed_categories
# this python file automatically creates categories if they don't exist
from django.core.management.base import BaseCommand
from apps.products.models import Category


def seed_categories():
    # Category.objects.all().delete()

    # checking if category exist to seed the categories
    if Category.objects.exists():
        print("⚠️ Categories already exist. Skipping seeding.")
        return

    print("🌱 Seeding categories...")

    # Top-level categories
    computer_laptop, _ = Category.objects.get_or_create(name='Computer & Laptop', parent=None)
    Category.objects.get_or_create(name='Laptops', parent=computer_laptop)
    Category.objects.get_or_create(name='Desktop Computers', parent=computer_laptop)
    Category.objects.get_or_create(name='Mini PCs', parent=computer_laptop)
    Category.objects.get_or_create(name='All-in-One PCs', parent=computer_laptop)

    # === Computer Accessories (child of Computer & Laptop) ===
    computer_accessories, _ = Category.objects.get_or_create(name='Computer Accessories', parent=None)
    Category.objects.get_or_create(name='Keyboards', parent=computer_accessories)
    Category.objects.get_or_create(name='Mice', parent=computer_accessories)
    Category.objects.get_or_create(name='Monitors', parent=computer_accessories)
    Category.objects.get_or_create(name='External Hard Drives', parent=computer_accessories)
    Category.objects.get_or_create(name='USB Hubs', parent=computer_accessories)

    # === smart phone ==
    smart_phone, _ = Category.objects.get_or_create(name='SmartPhone', parent=None)
    Category.objects.get_or_create(name='iPhone', parent=smart_phone)
    Category.objects.get_or_create(name='Samsung', parent=smart_phone)
    Category.objects.get_or_create(name='Xiaomi', parent=smart_phone)
    Category.objects.get_or_create(name='Oppo', parent=smart_phone)
    Category.objects.get_or_create(name='Huawei', parent=smart_phone)
    Category.objects.get_or_create(name='Infinix', parent=smart_phone)
    Category.objects.get_or_create(name='Vivo', parent=smart_phone)
    Category.objects.get_or_create(name='Tecno', parent=smart_phone)

    headphone, _ = Category.objects.get_or_create(name='Headphone', parent=None)
    Category.objects.get_or_create(name='Wired Headphones', parent=headphone)
    Category.objects.get_or_create(name='Wireless Headphones', parent=headphone)

    mobile_accessories, _ = Category.objects.get_or_create(name='Mobile Accessories', parent=None)
    Category.objects.get_or_create(name='Chargers', parent=mobile_accessories)
    Category.objects.get_or_create(name='Phone Cases', parent=mobile_accessories)
    Category.objects.get_or_create(name='Power Banks', parent=mobile_accessories)

    gaming_console, _ = Category.objects.get_or_create(name='Gaming Console', parent=None)
    Category.objects.get_or_create(name='PlayStation', parent=gaming_console)
    Category.objects.get_or_create(name='Xbox', parent=gaming_console)
    Category.objects.get_or_create(name='Nintendo', parent=gaming_console)

    camera_photo, _ = Category.objects.get_or_create(name='Camera & Photo', parent=None)
    Category.objects.get_or_create(name='DSLR', parent=camera_photo)
    Category.objects.get_or_create(name='Action Cameras', parent=camera_photo)
    Category.objects.get_or_create(name='Lenses', parent=camera_photo)

    tv_home_appliances, _ = Category.objects.get_or_create(name='TV & Homes Appliances', parent=None)
    Category.objects.get_or_create(name='Televisions', parent=tv_home_appliances)
    Category.objects.get_or_create(name='Refrigerators', parent=tv_home_appliances)
    Category.objects.get_or_create(name='Washing Machines', parent=tv_home_appliances)

    watch_accessories, _ = Category.objects.get_or_create(name='Watch & Accessories', parent=None)
    Category.objects.get_or_create(name='Smart Watches', parent=watch_accessories)
    Category.objects.get_or_create(name='Classic Watches', parent=watch_accessories)

    gps_navigation, _ = Category.objects.get_or_create(name='GPS & Navigation', parent=None)
    Category.objects.get_or_create(name='Car GPS', parent=gps_navigation)
    Category.objects.get_or_create(name='Hiking GPS', parent=gps_navigation)

    wearable_technologies, _ = Category.objects.get_or_create(name='Wearable Technology', parent=None)
    Category.objects.get_or_create(name='Fitness Trackers', parent=wearable_technologies)
    Category.objects.get_or_create(name='Smart Glasses', parent=wearable_technologies)

    print("✅ Categories and children seeded successfully.")
