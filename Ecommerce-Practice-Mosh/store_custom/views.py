from django.core.mail import send_mail,mail_admins,BadHeaderError,EmailMessage
from templated_mail.mail import BaseEmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from .tasks import notify_customers

def say_hello(request):
    notify_customers.delay('Hello')
    return HttpResponse("Hello Anil")




