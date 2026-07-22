from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.mail import send_mail,EmailMessage,send_mass_mail
from django.http import HttpResponse
# Create your views here.

def send_test_mail(request):
    subject="Welcome Mail"
    message="Welcome to our website"
    from_email='host email'
    recipient_list=['sender email']
    send_mail(subject,message,from_email,recipient_list)
    return HttpResponse("Mail send Successfully.")


def  send_test_email(request):
    subject="Welcome Mail"
    message=render_to_string(
        'welcome_email.html',
        {'username':'Abul',
        'course':'Django for beginners ',}
    )
    email=EmailMessage(subject,message,'your host email',['sender email'])
    email.content_subtype='html'
    email.send()
    return HttpResponse('Email send Successfully')


def send_test_bulk_email(request):
    message1=('Welcome to Culling Game','WE are glad to have you on here .','your host email',['sender email'])
    message2=('Welcome to Culling Game','WE are glad to have you on here .','your host email',['sender email 2'])
    message3=('Welcome to Culling Game','WE are glad to have you on here .','your host email',['sender email 3'])
    
    send_mass_mail((message1,message2,message3))
    return HttpResponse('Bulk Email Sent Successfully')