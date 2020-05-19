from django.db import models
from django.contrib.auth.models import AbstractUser

class Transaction(models.Model):
    account = models.CharField(max_length=100)
    summ = models.CharField(max_length=8)
    status = models.CharField(max_length=40)
    
    def __str__(self):
        return self.account

class GuideArticle(models.Model):
    name = models.CharField(max_length=255,null=True)
    text = models.TextField(null=True)
    image = models.FileField(upload_to='media/images',null=False)
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    mail_username = models.CharField(max_length=80)
    mail_password = models.CharField(max_length=100)
    use_tls = models.BooleanField(default=True)
    use_ssl = models.BooleanField(default=False)
    mail_host = models.CharField(max_length=80,null=True)
    mail_port = models.CharField(max_length=6,null=True)
    
    balance = models.FloatField(null=False,default=0.00)

    emails_amount = models.IntegerField(null=False,default=0)
    parse_tiu_amount = models.IntegerField(null=False,default=0)
    parse_avito_amount = models.IntegerField(null=False,default=0)
    
    sent = models.IntegerField(null=False,default=0)
    unsent = models.IntegerField(null=False,default=0)

    templates_amount = models.IntegerField(null=False,default=0)

    average_sum_amount = models.IntegerField(null=False,default=0)

    parsed = models.IntegerField(null=False,default=0)
    unparsed = models.IntegerField(null=False,default=0)

    is_admin = models.BooleanField(null=False,default=False)

    active_template = models.CharField(max_length=200,null=True)

class ClientParsing(models.Model):
    filename = models.CharField(null=True,max_length=100)
    url = models.CharField(max_length=255,null=False,default='')
    file_owner = models.CharField(max_length = 80,null=True)
    
    def __str__(self):
        return self.filename

class HtmlSend(models.Model):
    filename = models.CharField(null=True,max_length=100)
    our_file = models.FileField(upload_to='mail/templates/sending-templates',null=False)
    file_owner = models.CharField(max_length = 80,null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.filename

class HtmlSendFromConstructor(models.Model):
    filename = models.CharField(null=True,max_length=200)
    url = models.CharField(max_length=255,null=True)
    file_owner = models.CharField(max_length = 80,null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.filename

class FileToParse(models.Model):
    our_file = models.FileField(upload_to='media/files',null=False)
    file_owner = models.CharField(max_length = 80,null=True)



