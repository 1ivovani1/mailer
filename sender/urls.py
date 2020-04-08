from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from mail.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',render_main),
    path('login',login_page),
    path('logout',logout_page),
    path('main',main),
    path('register',register_page),
    path('buy_subscribe',buying_subscribition),
    path('success_pay',success_pay_render),
    path('guide',guide),
    path('preview',preview_template)
    ] + static('media/', document_root = 'media/')
