from django.core.management import BaseCommand

from users.models import Users


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = Users.objects.create(
            email='admin@sky.pro',
            first_name='Admin',
            last_name='Skypro',
            is_staff=True,
            is_superuser=True
        )
        user.set_password('123456')
        user.save()
