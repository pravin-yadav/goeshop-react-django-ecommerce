from django.urls import path, include
from .api import CreateUserAPI

urlpatterns = [
    path('register-user/', CreateUserAPI.as_view(), name='register-user'),
    path('register-superuser/', CreateUserAPI.as_view(), name='register-superuser'),
    path('register-staffuser/', CreateUserAPI.as_view(), name='register-staffuser'),
]
