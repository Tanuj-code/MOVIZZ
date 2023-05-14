from django.urls import path
from . import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
urlpatterns=[
    path('', views.home, name=""),
    path('rec', views.rec, name="rec"), 
    path('top', views.top, name="top"),
    path('contact', views.contact, name="contact"),
    path('favicon (3).ico', RedirectView.as_view(url=staticfiles_storage.url('image/favicon (3).ico')))
]