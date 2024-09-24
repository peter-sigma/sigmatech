# payment/email_helpers.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_success_email(user, order):
    # Subject and body for success email
    subject = f'Payment Successful for Order #{order.id}'
    message = render_to_string('payment/payment_success_email.html', {
        'user': user,
        'order': order,
    })
    
    # Send email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_failure_email(user):
    # Subject and body for failure email
    subject = 'Payment Failed'
    message = render_to_string('payment/payment_failure_email.html', {
        'user': user,
    })
    
    # Send email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )