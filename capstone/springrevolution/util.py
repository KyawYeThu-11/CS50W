from .models import User, Link, Message
from django.conf import settings
from django.template import loader
from django.core.mail import send_mail
import random

def password_validation(password):
    uppercase = 0
    lowercase = 0
    for c in password:
        if ord(c) in range(65, 91, 1):
            uppercase+=1
        elif ord(c) in range(97, 123, 1):
            lowercase+=1

    if len(password) < 8 or lowercase == 0 or uppercase == 0:
        return False
    else:
        return True

def mail_service(recipients, nickname):

    message_list = Message.objects.values_list('creator','message')
    email_message = random.choice(message_list)

    subject = 'Hello Comrade'
    message = ''
    email_from = settings.EMAIL_HOST_USER
    recipient_lists = [recipients]
    html_message = loader.render_to_string('springrevolution/our_message.html', {
        "nickname":nickname, 
        "creator":email_message[0],
        "email_body":email_message[1]
    })

    send_mail(subject, message, email_from, recipient_lists, fail_silently=False, html_message=html_message)
