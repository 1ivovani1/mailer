from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    mail_username = models.CharField(max_length=80)
    mail_password = models.CharField(max_length=100)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    mail_host = models.CharField(max_length=80,null=True)
    mail_port = models.CharField(max_length=6,null=True)
    
    twilio_account_sid = models.CharField(max_length=60,null=False,default='ACe449eb9c1ecabf1b928b78018404694d')
    twilio_auth_token = models.CharField(max_length=60,null=False,default='9d32bd3cee9faf93dab5038bb837cae5') 
    twilio_phone_number = models.CharField(max_length = 30,null=False,default='+12568343892')
    
    messages_amount = models.IntegerField(null=False,default=0)
    emails_amount = models.IntegerField(null=False,default=0)

    active_template = models.CharField(max_length=200,null=True)

    is_paid = models.BooleanField(default=False)

class HtmlSend(models.Model):
    filename = models.CharField(null=True,max_length=100)
    our_file = models.FileField(upload_to='mail/templates/sending-templates',null=False)
    file_owner = models.CharField(max_length = 80,null=True)
    is_active = models.BooleanField(default=False)

class FileToParse(models.Model):
    our_file = models.FileField(upload_to='media/files',null=False)
    file_owner = models.CharField(max_length = 80,null=True)


