from django.urls import path
from . import views
urlpatterns=[
    path('', views.home, name=""),
    path('rec', views.rec, name="rec"), 
    path('top', views.top, name="top"),
    path('contact', views.contact, name="contact"),
    
]