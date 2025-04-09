import threading
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

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
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    # Construct the URL to be sent in the email.
    confirm_url = request.build_absolute_uri(
        reverse('confirm-email', kwargs={'uidb64': uid, 'token': token})
    )
    
    subject = 'Confirm Your Email'
    message = (
        f"Hello {user.username},\n\n"
        "Thank you for signing up. Please confirm your email address by clicking the link below:\n"
        f"{confirm_url}\n\n"
        "If you did not sign up, please ignore this email."
    )
    send_email_async(subject, message, [user.email])
