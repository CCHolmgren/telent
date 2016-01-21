from django.apps import AppConfig
from .models import Profile
from django.contrib.auth.models import User

from allauth.account.signals import email_confirmed

def callback(email_address):
    user = User.objects.get(email=email_address)
    Profile.objects.get_or_create(user=user)

class TelentappConfig(AppConfig):
    name = 'telentapp'

    def ready(self):
        print("Registering email_confirmed.connect callback")
        email_confirmed.connect(callback)
