from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Creates the first admin user'

    def handle(self, *args, **kwargs):
        email = 'admin@yoursite.com'
        password = 'ChangeMe123!'
        username = 'superadmin'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING('Admin already exists.'))
            return

        User.objects.create_user(
            email=email,
            username=username,
            password=password,
            role='ADMIN',
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(self.style.SUCCESS(f'First admin created: {email}'))


        