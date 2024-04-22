from django.urls import include, path, re_path


from . import views
from django.contrib.auth.decorators import login_required
from rest_framework import routers

app_name = 'authentication'

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
    re_path(r'^signout', views.signout, name='signout'),
]
