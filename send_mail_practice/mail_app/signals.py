from django.dispatch import receiver
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save,sender=User)
def send_welcome_mail_to_user(sender,instance,created,**kwargs):
    if created and instance.email :
        print(f"New User created")
        subject="Welcome to Django"
        message=f'Hi {instance.username}. We are glad that you sign up to this course.'
        from_email='host email'
        recipient_list=[instance.email]
        send_mail(subject,message,from_email,recipient_list)
        print("Email Sent Successfully.")
    elif instance.email:
        print(f"New User updated and email provided ")
        subject="Welcome to Django"
        message=f'Hi {instance.username}. We are glad that you sign up to this course.'
        from_email='host email'
        recipient_list=[instance.email]
        send_mail(subject,message,from_email,recipient_list)
        print("Email Sent Successfully.")