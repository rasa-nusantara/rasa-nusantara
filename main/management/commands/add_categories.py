from django.core.management.base import BaseCommand
from main.models import Category

class Command(BaseCommand):
    help = 'Adds predefined categories to the database'

    def handle(self, *args, **kwargs):
        categories = [
            "Gudeg", "Oseng", "Bakpia", "Sate", "Sego Gurih",
            "Wedang", "Lontong", "Rujak Cingur", "Mangut Lele", "Ayam", "Lainnya"
        ]

        for category_name in categories:
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category_name}' created."))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category_name}' already exists."))

        self.stdout.write(self.style.SUCCESS("Categories added successfully!"))
