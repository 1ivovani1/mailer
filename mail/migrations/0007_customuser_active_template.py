# Generated by Django 2.2.4 on 2020-03-09 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0006_htmlsend_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='active_template',
            field=models.CharField(max_length=200, null=True),
        ),
    ]