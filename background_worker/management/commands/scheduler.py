from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Runs the background worker scheduler'

    def add_arguments(self, parser):
        # Optional: Add positional arguments or optional flags here
        parser.add_argument('--now', action='store_true', help='Run immediately')

    def handle(self, *args, **options):
        # Your execution logic goes here
        if options['now']:
            self.stdout.write(self.style.SUCCESS('Running scheduler immediately...'))
        else:
            self.stdout.write(self.style.SUCCESS('Starting standard scheduler...'))
