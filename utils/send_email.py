from django.core.mail import send_mail
from django.conf import settings

sender_email = getattr(settings, 'EMAIL_HOST_USER', None)
def send_email(subject,body,recipient_email):
    sender_email = sender_email
    send_mail(
            subject,
            body,
            sender_email,
            [recipient_email],
            fail_silently=False,
    )
