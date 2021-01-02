from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils.timezone import now

from ...models import Rule


class Command(BaseCommand):
    help = 'Trims the blacklist'

    def add_arguments(self, parser):
        parser.add_argument('--ip', type=str,
            help='created days ago; default: 0')

    def handle(self, *args, **options):
        self.stdout.write('Deleting expired rules')

        ip = timedelta(days=options['ip'])

        rules = Rule.objects.filter(address=(ip))

        deleted = rules.delete()
        num_deleted = deleted[1].get('%s.%s' % (Rule._meta.app_label, Rule._meta.object_name), 0)

        self.stdout.write(self.style.SUCCESS('Deleted %d rule(s).' % num_deleted))
