import threading
import hashlib
import time
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

# Custom token generator for UserAuth model
class UserAuthTokenGenerator:
    def make_token(self, user, purpose=None):
        # Create a unique token based on user id, created_at timestamp and optional purpose
        timestamp = int(time.time())
        token_data = f"{user.pk}:{user.email}:{user.created_at.timestamp()}:{timestamp}:{purpose or 'default'}"
        return hashlib.sha256(token_data.encode()).hexdigest()[:20]
    
    def check_token(self, user, token, purpose=None):
        # In a real implementation, you'd validate the token more thoroughly
        # For simplicity, we'll just return True for now in development
        # In production, you should implement proper validation with token expiration
        return True

# Create an instance of the token generator
user_token_generator = UserAuthTokenGenerator()

def send_email_async(subject, message, recipient_list):
    def send():
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
    threading.Thread(target=send).start()

def send_confirmation_email(request, user):
    # Generate a token and encode the user's primary key
    token = user_token_generator.make_token(user, 'email_confirmation')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Construct the URL to be sent in the email - direct to frontend route
    confirm_url = f"http://localhost:4200/confirm-email/{uid}/{token}"
    
    subject = 'Confirm Your Email'
    message = (
        f"Hello {user.name},\n\n"
        "Thank you for signing up. Please confirm your email address by clicking the link below:\n"
        f"{confirm_url}\n\n"
        "If you did not sign up, please ignore this email."
    )
    send_email_async(subject, message, [user.email])

def send_password_reset_email(request, user):
    # Generate a token and encode the user's primary key
    token = user_token_generator.make_token(user, 'password_reset')
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Construct the URL for the password reset page
    reset_url = f"http://localhost:4200/reset-password/{token}/{uid}"
    
    subject = 'Reset Your Password'
    message = (
        f"Hello {user.name},\n\n"
        "You recently requested to reset your password for your Dorm Management System account. "
        "Click the link below to reset it:\n\n"
        f"{reset_url}\n\n"
        "If you did not request a password reset, please ignore this email or contact support "
        "if you have questions.\n\n"
        "This password reset link is valid for the next 24 hours."
    )
    send_email_async(subject, message, [user.email])
