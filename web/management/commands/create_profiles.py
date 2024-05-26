from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from web.models import UserProfile


class Command(BaseCommand):
    help = 'Create missing user profiles'

    def handle(self, *args, **kwargs):
        users = User.objects.filter(profile__isnull=True)
        for user in users:
            UserProfile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created missing user profiles'))
