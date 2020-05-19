from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf.urls import handler404,handler500

from mail.views import *

# handler404 = 'mail.views.e_handler404'
# handler500 = 'mail.views.e_handler500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',render_main),
    path('login',login_page),
    path('logout',logout_page),
    path('main',main),
    path('register',register_page),
    path('buy_subscribe',buying_subscribition),
    path('success_pay',success_pay_render),
    path('fail_pay',fail_pay_render),
    path('guide',guide),
    path('preview',preview_template),
    path('preview_from_constructor',preview_template_from_constructor),
    path('request',request_check),
    path('add_guide',adding_guide),
    path('editor',editor)
    ] + static('media/', document_root = 'media/')
