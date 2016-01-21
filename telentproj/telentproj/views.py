from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

def profile(request):
    return redirect(reverse('user_profile', kwargs={'username':request.user}))