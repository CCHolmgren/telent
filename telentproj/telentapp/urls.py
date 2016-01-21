"""telentproj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include

from telentapp import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^images/', include([
        url(r'^$', views.PopularView.as_view()),
        url(r'^latest/$', views.LatestImagesView.as_view(), name='latest_images'),
        url(r'^upload/$', views.UploadImageView.as_view(), name='upload'),
        url(r'^popular/$', views.PopularView.as_view(), name='popular'),
        url(r'^(?P<slug>[a-zA-Z0-9_-]+)/', include([
            url(r'^$', views.ImageView.as_view(), name='image'),
            url(r'^edit/$', views.ImageEditView.as_view(), name='edit_image'),
            url(r'^report/$', views.ImageReportCreationView.as_view(), name='report')
        ]))
    ])),
    url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.UserProfile.as_view(), name='user_profile'),
]
