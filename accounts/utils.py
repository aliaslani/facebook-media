from django.core.mail import send_mail
from django.conf import settings


def send_welcome_email(user):
    send_mail(
        subject="Welcome!",
        message=f"Hello {user.username}, welcome!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )