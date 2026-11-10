from pathlib import Path

from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command


class Command(BaseCommand):
    help = 'Load the JSON problem catalog into Django problem models.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=Path,
            default=Path(settings.PROBLEM_FIXTURE_PATH),
            help='Path to the Django JSON fixture containing problems and test cases.',
        )

    def handle(self, *args, **options):
        fixture_path = options['path']
        if not fixture_path.is_file():
            raise CommandError(f'Problem fixture not found: {fixture_path}')

        try:
            call_command('loaddata', str(fixture_path), verbosity=0)
        except Exception as exc:
            raise CommandError(
                f'Unable to load problem fixture {fixture_path}: {exc}'
            ) from exc

        self.stdout.write(
            self.style.SUCCESS(f'Loaded problem catalog from {fixture_path}')
        )
