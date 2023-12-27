from django.core.management.base import BaseCommand
from django.core.mail import send_mail

class Command(BaseCommand):
    help = 'Sends a test email using Django.'

    def handle(self, *args, **options):
        subject = 'Subject of the Test Email'
        body = 'Body of the Test Email'
        sender_email = 'no-reply@sunrayops.com'
        recipient_email = 'rajaatifrasheed777@gmail.com'

        send_mail(
            subject,
            body,
            sender_email,
            [recipient_email],
            fail_silently=False,
        )

        self.stdout.write(self.style.SUCCESS('Test email sent successfully!'))
