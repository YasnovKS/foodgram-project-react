import csv

from django.core.management.base import BaseCommand, CommandError

from food_app.models import Ingredient, Tag


class Command(BaseCommand):
    '''This is a class for import data from csv file to database.'''

    def handle(self, *args, **options):
        try:
            with open('../data/ingredients.csv', 'r') as file:
                data = csv.reader(file, delimiter=',')
                for row in data:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        unit=row[1]
                    )
            with open('../data/tags.csv', 'r') as file:
                data = csv.reader(file, delimiter=',')
                for row in data:
                    Tag.objects.get_or_create(
                        title=row[0],
                        color=row[1],
                        slug=row[2]
                    )
        except Exception:
            raise CommandError('Import error')

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
