"""
A simple utility script to directly activate a user account by user_id.
Run this script with the Django shell:
python manage.py shell < api/activate_user.py
"""

from api.models import UserAuth
import sys

def activate_user_by_id(user_id):
    try:
        user = UserAuth.objects.get(user_id=user_id)
        print(f"Found user: {user.user_id}")
        print(f"Current is_active status: {user.is_active}")
        
        user.is_active = True
        user.save()
        
        # Verify the change
        user.refresh_from_db()
        print(f"Updated is_active status: {user.is_active}")
        
        return True
    except UserAuth.DoesNotExist:
        print(f"User with ID {user_id} not found")
        return False
    except Exception as e:
        print(f"Error activating user: {e}")
        return False

# Check if a user ID was provided
if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_id = sys.argv[1]
        activate_user_by_id(user_id)
    else:
        print("Usage: python manage.py shell < api/activate_user.py [user_id]")
        # Just as a test, let's try to list all users
        users = UserAuth.objects.all()
        if users.exists():
            print("\nAll users:")
            for user in users:
                print(f"ID: {user.user_id}, Email: {user.email}, Active: {user.is_active}")
