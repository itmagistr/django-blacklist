from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import F
from django.utils.timezone import now

from ...models import Rule


class Command(BaseCommand):
    help = 'Remove an IP from the blacklist'

    def add_arguments(self, parser):
        parser.add_argument('--ip', type=str,
            help='IP Address to remove')

    def handle(self, *args, **options):
        self.stdout.write('Deleting IP rules')

        rules = Rule.objects.filter(address=(options['ip']))

        deleted = rules.delete()
        num_deleted = deleted[1].get('%s.%s' % (Rule._meta.app_label, Rule._meta.object_name), 0)

        self.stdout.write(self.style.SUCCESS('Deleted %d rule(s).' % num_deleted))
