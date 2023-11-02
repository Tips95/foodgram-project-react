import json
import os

from django.core.management.base import BaseCommand
from foodgram.settings import BASE_DIR
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    def import_ingredient_from_file(self):
        data_folder = os.path.join(BASE_DIR, 'data')
        for data_file in os.listdir(data_folder):
            with open(
                os.path.join(data_folder, data_file), encoding='utf-8'
            ) as data_file:
                data = json.loads(data_file.read())
                for data_object in data:
                    name = data_object.get('name', None)
                    measurement_unit = data_object.get(
                        'measurement_unit', None
                    )

                    try:
                        ingredient, created = (
                            Ingredient.objects.get_or_create(
                                name=name,
                                measurement_unit=measurement_unit,)
                        )
                        if created:
                            ingredient.save()
                            display_format = (
                                "\ningredient, {}, has been saved."
                            )
                            print(display_format.format(ingredient))
                    except Exception as ex:
                        print(str(ex))
                        msg = (
                            "\n\nSomething went wrong saving this ingredient:"
                            " {}\n{}".format(name, str(ex))
                        )
                        print(msg)

    def import_tag(self):
        data = [
            {'name': 'Завтрак', 'color': '#FF5733', 'slug': 'breakfast'},
            {'name': 'Обед', 'color': '#33FF57', 'slug': 'lunch'},
            {'name': 'Ужин', 'color': '#5733FF', 'slug': 'supper'},
        ]
        for data_object in data:
            name = data_object.get('name', None)
            color = data_object.get('color', None)
            slug = data_object.get('slug', None)
            try:
                tag, created = (
                    Tag.objects.get_or_create(
                        name=name,
                        color=color,
                        slug=slug
                    )
                )
                if created:
                    tag.save()
                    display_format = (
                        "\ntag, {}, has been saved."
                    )
                    print(display_format.format(tag))
            except Exception as ex:
                print(str(ex))
                msg = (
                    "\n\nSomething went wrong saving this tag:"
                    " {}\n{}".format(name, str(ex))
                )
                print(msg)

    def handle(self, *args, **options):
        """
        Call the function to import data
        """
        self.import_ingredient_from_file()
        self.import_tag()
