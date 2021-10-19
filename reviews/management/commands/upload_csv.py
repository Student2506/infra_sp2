import csv
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from reviews.models import (Category, Review, Title,  # noqa
                            User)


class Command(BaseCommand):
    help = ('Categories needs to be processed before Titles, Titles and Genres'
            ' needs to be processed before linking...')

    def add_arguments(self, parser):
        # Postional arguments
        parser.add_argument('model_name')

        # Named (optional) arguments
        parser.add_argument('--filename', help='file to upload to DB')

    def handle(self, *args, **options):
        model = None
        model_name = options['model_name']
        try:
            model = apps.get_model('reviews', model_name)
        except LookupError:
            raise CommandError(f"Model: '{model_name}' doesn't exist")

        if options['filename'] is not None:
            upload_file = (Path(settings.BASE_DIR) / 'static/data'
                           / options['filename'])
        else:
            upload_file = (Path(settings.BASE_DIR) / 'static/data'
                           / f'{model_name}.csv')

        if not upload_file.exists():
            print(f"File {upload_file.name} doesn't exist"
                  ", use '--filename' to specify right one.")
            return
        with open(upload_file, encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader, None)
            self.fill_database(model, reader, header)

            print(f'Done: {model.objects.all()}')

    def fill_database(self, model, cursor, header):

        if model.__name__.lower() == 'title':

            for r in cursor:
                each_row = dict(zip(header[1:], r[1:]))
                category_instance = Category.objects.get(pk=r[-1])
                each_row['category'] = category_instance
                current_row = model.objects.create(**each_row)
                current_row.save()

        elif model.__name__.lower() in [
            'category', 'genre', 'user'
        ]:

            for r in cursor:
                each_row = dict(zip(header[1:], r[1:]))
                current_row = model.objects.create(**each_row)
                current_row.save()

        elif model.__name__.lower() == 'review':

            for r in cursor:
                each_row = dict(zip(header[1:], r[1:]))
                user_instance = User.objects.get(pk=r[3])
                title_instance = Title.objects.get(pk=r[1])
                each_row['author'] = user_instance
                each_row['title_id'] = title_instance
                current_row = model.objects.create(**each_row)

        elif model.__name__.lower() == 'comment':
            for r in cursor:
                each_row = dict(zip(header[1:], r[1:]))
                user_instance = User.objects.get(pk=r[3])
                review_instance = Review.objects.get(pk=r[1])
                each_row['author'] = user_instance
                each_row['review_id'] = review_instance
                current_row = model.objects.create(**each_row)
