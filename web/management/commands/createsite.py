from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from decouple import config


class Command(BaseCommand):
    help = 'Create or update the default site'

    def handle(self, *args, **kwargs):
        domain = config('SITE_DOMAIN', default='localhost')
        name = config('SITE_NAME', default='localhost')
        site_id = config('SITE_ID', default=1, cast=int)

        Site.objects.update_or_create(
            id=site_id,
            defaults={
                'domain': domain,
                'name': name,
            }
        )
        self.stdout.write(self.style.SUCCESS(f'Successfully set site to {domain}'))
