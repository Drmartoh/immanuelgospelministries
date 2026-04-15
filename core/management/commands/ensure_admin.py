import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create or reset the default superuser for /admin/ (set IGM_ADMIN_* env vars to override)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-password",
            action="store_true",
            help="If the user already exists, reset password and staff flags.",
        )

    def handle(self, *args, **options):
        username = os.getenv("IGM_ADMIN_USERNAME", "admin")
        email = os.getenv("IGM_ADMIN_EMAIL", "admin@immanuelgospel.org")
        password = os.getenv("IGM_ADMIN_PASSWORD", "Immanuel@Admin2026")

        User = get_user_model()
        user = User.objects.filter(username=username).first()
        did_set_password = False

        if user is None:
            User.objects.create_superuser(username=username, email=email, password=password)
            did_set_password = True
            self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
        elif options["reset_password"]:
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.email = email
            user.save()
            did_set_password = True
            self.stdout.write(self.style.SUCCESS(f'Updated superuser "{username}" (password reset).'))
        else:
            self.stdout.write(
                self.style.WARNING(
                    f'User "{username}" already exists. Log in or run: python manage.py ensure_admin --reset-password'
                )
            )
            return

        if did_set_password:
            self.stdout.write(f"  Username: {username}")
            self.stdout.write(f"  Password: {password}")
            self.stdout.write(self.style.WARNING("  Change this password after first login on any public server."))
