from celery import shared_task
from django.core.mail import EmailMessage
from django.conf import settings

@shared_task
def send_email_async(subject, to, body, html=False):
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to if isinstance(to, list) else [to],
    )
    if html:
        email.content_subtype = 'html'

    print(email.__str__())
    email.send()
