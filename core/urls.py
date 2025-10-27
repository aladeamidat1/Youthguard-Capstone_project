

from django.urls import path
from .views import current_user, create_company, create_user

urlpatterns = [

    path('register/', create_user, name='create-user'),
    path('current-user/', current_user, name='current-user'),
    path('create-company/', create_company, name='create-company'),
]