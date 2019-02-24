from django.core.management.base import (BaseCommand, CommandError)
from myadmin.backenddb import (insert_custom_areas, insert_default_categories)


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        # parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        # load default areas
        insert_custom_areas('Bangalore', 'Karnataka', 'India')
        # load default categories
        insert_default_categories()
