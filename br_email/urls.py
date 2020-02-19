from django.urls import path
from . import views
from .views import EventListView


urlpatterns = [
    path('', views.home, name='br_email_home'),
    # path('register/', views.register, name='br_email_register'),
    # path('profile/', views.profile, name='br_email_profile'),
    path('events/', EventListView.as_view(), name='br_email_events'),
    path('contact/', views.contact, name='br_email_contact'),
]

