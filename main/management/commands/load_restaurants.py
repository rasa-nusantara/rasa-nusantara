import json
import os
from django.core.management.base import BaseCommand
from main.models import Restaurant, MenuItem
from django.db import transaction

class Command(BaseCommand):
    help = 'Load restaurant and menu data from a JSON file into the database.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            help='Indicate the JSON file to load data from.',
            required=True
        )

    def handle(self, *args, **options):
        file_path = options['file']

        if not os.path.exists(file_path):
            self.stderr.write(self.style.ERROR(f"File '{file_path}' does not exist."))
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"Invalid JSON format: {e}"))
            return

        if not isinstance(data, list):
            self.stderr.write(self.style.ERROR("JSON data must be a list of restaurant objects."))
            return

        self.stdout.write(self.style.SUCCESS(f"Starting to load {len(data)} restaurants..."))

        with transaction.atomic():
            for entry in data:
                try:
                    name = entry.get("Nama Restoran", "").strip()
                    location = entry.get("Lokasi Restoran", "").strip()
                    average_price = entry.get("Harga Rata-Rata Makanan di Toko (Rp)", 0)
                    rating = entry.get("Rating Toko", 0.0)
                    variasi_makanan = entry.get("Variasi Makanan", "")

                    if not name or not location:
                        self.stderr.write(self.style.WARNING(f"Skipping entry with missing name or location: {entry}"))
                        continue

                    # Create or get Restaurant
                    restaurant, created = Restaurant.objects.get_or_create(
                        name=name,
                        location=location,
                        defaults={
                            'average_price': average_price,
                            'rating': rating
                        }
                    )

                    if not created:
                        # Update fields if necessary
                        updated = False
                        if restaurant.average_price != average_price:
                            restaurant.average_price = average_price
                            updated = True
                        if restaurant.rating != rating:
                            restaurant.rating = rating
                            updated = True
                        if updated:
                            restaurant.save()
                            self.stdout.write(self.style.SUCCESS(f"Updated Restaurant: {name}"))

                    # Process Menu Items
                    menu_items = [item.strip() for item in variasi_makanan.split(',') if item.strip()]
                    for menu_name in menu_items:
                        menu_item, menu_created = MenuItem.objects.get_or_create(
                            restaurant=restaurant,
                            name=menu_name
                        )
                        if menu_created:
                            self.stdout.write(self.style.SUCCESS(f"  - Added MenuItem: {menu_name}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"  - MenuItem already exists: {menu_name}"))

                    self.stdout.write(self.style.SUCCESS(f"Successfully processed Restaurant: {name}"))

                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Error processing entry {entry}: {e}"))

        self.stdout.write(self.style.SUCCESS("Data loading complete."))