import logging

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from datasets.imports.temperature import import_temperature


log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Import datasets relevant for Energie transitie project'

    # object store statische bronnen
    bronnen = {
        'temperature': import_temperature
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--dir', dest='dir', type=str,
            help='Directory to load datafiles from (default /data).')

        # for every bron add flag.
        for key in self.bronnen.keys():
            parser.add_argument(
                f'--{key}', default=False,
                action='store_true', help=f'Load {key}')

    def handle(self, *args, **options):
        target_dir = options['dir'] if options['dir'] is not None else '/data'
        log.info('Downloading / Importing from %s', target_dir)

        # import single bron
        for bron, import_function in self.bronnen.items():
            if options.get(bron):
                import_function(target_dir)
                return

        # if no aguments is given load ALL static sources
        for bron, import_function in self.bronnen.items():
                import_function(target_dir)
