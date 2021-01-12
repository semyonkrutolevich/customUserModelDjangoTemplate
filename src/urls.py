from django import urls
from django.contrib import admin
from django.conf.urls import include
from django.urls import path

from accounts.views import register_view, login_view, logout_view



admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]

