"""Seed Velora with starter categories. Usage:
python manage.py seed_velora
"""
from django.core.management.base import BaseCommand
from shop.models import Category

CATEGORIES = [
    "Dresses", "Sarees & Lehengas", "Suits & Tuxedos",
    "Accessories", "Bags", "Jewellery", "Shoes", "Outerwear",
]


class Command(BaseCommand):
    help = "Populate the database with starter fashion categories."

    def handle(self, *args, **options):
        created = 0
        for name in CATEGORIES:
            _, was_created = Category.objects.get_or_create(name=name)
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Categories ready. {created} newly created."))