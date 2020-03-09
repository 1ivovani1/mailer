from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from mail.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login',login_page),
    path('logout',logout_page),
    path('',main)
    ] + static('media/', document_root = 'media/')
