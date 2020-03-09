from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    mail_username = models.CharField(max_length=80)
    mail_password = models.CharField(max_length=100)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    mail_host = models.CharField(max_length=80,null=True)
    mail_port = models.CharField(max_length=6,null=True)
    
    twilio_account_sid = models.CharField(max_length=60,null=True)
    twilio_auth_token = models.CharField(max_length=60,null=True) 
    twilio_phone_number = models.CharField(max_length = 30,null=True)
    
    active_template = models.CharField(max_length=200,null=True)

class HtmlSend(models.Model):
    filename = models.CharField(null=True,max_length=100)
    our_file = models.FileField(upload_to='mail/templates/sending-templates',null=False)
    file_owner = models.CharField(max_length = 80,null=True)
    is_active = models.BooleanField(default=False)

class FileToParse(models.Model):
    our_file = models.FileField(upload_to='media/files',null=False)
    file_owner = models.CharField(max_length = 80,null=True)


