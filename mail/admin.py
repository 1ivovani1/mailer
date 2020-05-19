from django.contrib import admin
from .models import *

admin.site.register(HtmlSend)
admin.site.register(FileToParse)
admin.site.register(CustomUser)
admin.site.register(ClientParsing)
admin.site.register(GuideArticle)
admin.site.register(HtmlSendFromConstructor)