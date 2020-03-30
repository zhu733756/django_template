from django.conf.urls import url
from django.urls import include
from .auth import obtain_expiring_auth_token
from .views import *

urlpatterns = [
    url(r'user/auth', obtain_expiring_auth_token),
]
