from django.core.management.base import BaseCommand
from api.models import UserAuth

class Command(BaseCommand):
    help = 'Manually activate a user account by user_id'

    def add_arguments(self, parser):
        parser.add_argument('user_id', nargs='?', type=str, help='The user ID to activate')
        parser.add_argument('--list', action='store_true', help='List all users and their activation status')

    def handle(self, *args, **options):
        user_id = options.get('user_id')
        list_users = options.get('list')

        if list_users:
            self.list_all_users()
            return

        if not user_id:
            self.stdout.write(self.style.ERROR('Error: You must provide a user_id'))
            self.stdout.write('Usage: python manage.py activate_user [user_id]')
            self.stdout.write('Usage: python manage.py activate_user --list')
            return

        self.activate_user(user_id)

    def activate_user(self, user_id):
        try:
            user = UserAuth.objects.get(user_id=user_id)
            self.stdout.write(f"Found user: {user.user_id}")
            self.stdout.write(f"Current is_active status: {user.is_active}")
            
            user.is_active = True
            user.save()
            
            # Verify the change
            user.refresh_from_db()
            self.stdout.write(self.style.SUCCESS(f"Updated is_active status: {user.is_active}"))
            
        except UserAuth.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error activating user: {e}"))

    def list_all_users(self):
        users = UserAuth.objects.all()
        if users.exists():
            self.stdout.write(self.style.SUCCESS("\nAll users:"))
            self.stdout.write(f"{'ID':<15} {'Name':<20} {'Email':<30} {'Active':<10}")
            self.stdout.write("-" * 75)
            for user in users:
                active_status = "✓" if user.is_active else "✗"
                self.stdout.write(f"{user.user_id:<15} {user.name:<20} {user.email:<30} {active_status:<10}")
        else:
            self.stdout.write(self.style.ERROR("No users found in the database"))