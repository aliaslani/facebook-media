from django.contrib.auth.models import User
from django_huey import db_task, task
from django.core.mail import send_mail
from django.conf import settings

@task(queue='emails')
def send_welcome_email(user_email):
    send_mail(
        subject="Welcome to Django Huey",
        message="Welcome to Django Huey",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )



