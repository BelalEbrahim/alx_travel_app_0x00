import random
from django.core.management.base import BaseCommand
from listings.models import Listing

class Command(BaseCommand):
    help = 'Seed the database with sample listings'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        sample_data = [
            {'title': 'Beachside Bungalow', 'description': 'Cozy bungalow by the sea', 'price_per_night': 120.00, 'address': '123 Ocean Drive'},
            {'title': 'Mountain Cabin', 'description': 'Rustic cabin in the mountains', 'price_per_night': 90.00, 'address': '456 Pine Street'},
            {'title': 'City Apartment', 'description': 'Modern apartment downtown', 'price_per_night': 150.00, 'address': '789 Main Street'},
        ]
        for data in sample_data:
            Listing.objects.create(**data)
        self.stdout.write(self.style.SUCCESS('Database seeded successfully.'))
