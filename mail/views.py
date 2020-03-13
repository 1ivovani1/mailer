from django.shortcuts import render,redirect
from django import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages

from django.core.mail import send_mail,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail

from .models import *

import time
from twilio.rest import Client

import json

class LoginValidation(forms.Form):
    login = forms.CharField(max_length = 50)
    password = forms.CharField(min_length = 2)


def get_contacts(filename):
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            emails.append(a_contact.split()[1])
    return emails


def main(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':

        templates_to_render = []

        user = request.user
        all_user_templates = HtmlSend.objects.filter(file_owner = user).all()

        for template in all_user_templates:
            f = open(f'{template.our_file.url}')
            template.filename = template.our_file.url[33:]
            template.save()
            templates_to_render.append(f.read())
            f.close()
        
        return render(request,'main.html',{'templates_to_render':templates_to_render,'all_user_templates':all_user_templates})
    
    if request.method == 'POST':

        if ('html_file_download' in request.POST) or ('template_url'  in request.POST):
            body = request.POST
        else:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)

        if 'html_file_download' in request.POST:
            our_file = request.FILES['html_file']
            filename = request.POST.get('dowload_filename')

            prev_active = HtmlSend.objects.filter(is_active = True).first()
            prev_active.is_active = False
            prev_active.save() 

            new_file = HtmlSend()
            new_file.filename = filename
            new_file.our_file = our_file
            new_file.is_active = True
            new_file.file_owner = request.user
            new_file.save()

            user = request.user
            user.active_template = new_file.our_file.url
            user.save()


            return redirect('/')
        
        if ('template_url' in request.POST) and ('template_id' in request.POST):
            template_id = request.POST.get('template_id')
            template_url = request.POST.get('template_url')

            active_template = HtmlSend.objects.filter(id=int(template_id)).first()
            active_template.is_active = True
            active_template.save()

            user = request.user
            user.active_template = template_url
            user.save()
            
            return redirect('/')

        
        if 'myself' in body:
            if request.user.active_template != None:
                email = body.get('email')
                subject = body.get('subject')

                sending_file = request.user.active_template


                connection = get_connection(username=request.user.mail_username,password=request.user.mail_password,host=request.user.mail_host,port=request.user.mail_port,use_tls=request.user.use_tls,use_ssl=request.user.use_ssl)

                html_message = render_to_string(f'{sending_file}'[15:])
                plain_message = strip_tags(html_message)
                mail.send_mail(subject,plain_message,request.user.mail_username,[email],html_message=html_message,connection=connection)
                messages.add_message(request, messages.ERROR, 'Message is sent!')
            else:
                messages.add_message(request, messages.ERROR, 'You have to choose a sending template!')
            return redirect('/')

        if 'sending_from_txt' in body:
            subject = body.get('subject')

            if 'txt_file' in request.FILES:
                our_file = FileToParse()
                our_file.our_file = request.FILES['txt_file']
                our_file.file_owner = request.user.username
                our_file.save()
            
            if request.user.active_template != None:
                sending_file = request.user.active_template
                file_to_parse = FileToParse.objects.filter(file_owner = request.user.username).last()

                emails = get_contacts(f'{file_to_parse.our_file.url}')

                connection = get_connection(username=request.user.mail_username,password=request.user.mail_password,host=request.user.mail_host,port=request.user.mail_port,use_tls=request.user.use_tls,use_ssl=request.user.use_ssl)

                html_message = render_to_string(f'{sending_file}'[15:])
                plain_message = strip_tags(html_message)
                mail.send_mail(subject,plain_message,request.user.mail_username,emails,html_message=html_message,connection=connection)
                messages.add_message(request, messages.ERROR, 'Messages are sent!')
                
                file_to_parse.delete()
            else:
                messages.add_message(request, messages.ERROR, 'You have to choose a sending template!')
            return redirect('/')

        if 'config' in body:
            host = body.get('host')
            username = body.get('username')
            password = body.get('password')
            port = body.get('port')
            tls = body.get('use_tls')
            ssl = body.get('use_ssl')

            user = request.user
            user.mail_username = username
            user.mail_password = password
            user.mail_host = host
            user.mail_port = port
            if tls == None:
                user.use_tls = False
            elif tls == 'on':
                user.use_tls = True

            if ssl == None:
                user.use_ssl = False
            elif ssl == 'on':
                user.use_ssl = True

            user.save()
            messages.add_message(request, messages.ERROR, 'Email config is changed!')
            
            return redirect('/')

        if 'one_number_send' in body:
            phone_number = body.get('phone_number')
            message_body = body.get('one_message_body')

            account_sid = request.user.twilio_account_sid
            auth_token = request.user.twilio_auth_token
            from_who_send = request.user.twilio_phone_number

            client = Client(account_sid, auth_token) 
            message = client.messages \
                .create(
                     body=message_body,
                     from_=from_who_send,
                     to=phone_number
                 )
            messages.add_message(request, messages.ERROR, 'Messages are sent!')
            return redirect('/')

        if 'txt_number_send' in body:
            if 'txt_file' in request.FILES:
                our_file = FileToParse()
                our_file.our_file = request.FILES['txt_file']
                our_file.file_owner = request.user.username
                our_file.save()

            file_to_parse = FileToParse.objects.filter(file_owner = request.user.username).last()
            message_body = body.get('one_message_body')
            phone_numbers = get_contacts(f'{file_to_parse.our_file.url}')

            account_sid = request.user.twilio_account_sid
            auth_token = request.user.twilio_auth_token
            from_who_send = request.user.twilio_phone_number

            client = Client(account_sid, auth_token) 

            for number in phone_numbers:
            
                message = client.messages \
                    .create(
                        body=message_body,
                        from_=from_who_send,
                        to=number
                    )
            messages.add_message(request, messages.ERROR, 'Messages are sent!')
            file_to_parse.delete()
            return redirect('/')
        
        if 'twilio_config' in body:
            twilio_number = body.get('twilio_number')
            twilio_account_sid = body.get('twilio_sid')
            twilio_auth_token = body.get('twilio_token')

            user = request.user
            user.twilio_account_sid = twilio_account_sid
            user.twilio_auth_token = twilio_auth_token
            user.twilio_phone_number = twilio_number
            user.save()
            messages.add_message(request, messages.ERROR, 'Twilio messaging config is changed!')
            return redirect('/')
        



def logout_page(request):
    logout(request)
    return redirect('/login')


def login_page(request):
    if request.method == 'GET':
        return render(request,'login.html')
    
    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():
            
            messages.add_message(request, messages.ERROR, 'Data is incorrect!')
            return redirect('/login')

        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)


        if user is None:
            messages.add_message(request, messages.ERROR, 'Data is incorrect!')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')

