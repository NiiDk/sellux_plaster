from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'Initialize or update the Django Site object'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='selluxplaster.com',
            help='Domain name for the Site object',
        )
        parser.add_argument(
            '--name',
            type=str,
            default='Sellux Plaster',
            help='Display name for the Site object',
        )

    def handle(self, *args, **options):
        domain = options['domain']
        name = options['name']
        
        site, created = Site.objects.get_or_create(
            id=1,
            defaults={
                'domain': domain,
                'name': name,
            }
        )
        
        if not created:
            site.domain = domain
            site.name = name
            site.save()
            self.stdout.write(self.style.SUCCESS(f'Updated Site: {site.domain}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Created Site: {site.domain}'))
