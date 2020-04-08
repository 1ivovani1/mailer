from django.shortcuts import render,redirect,HttpResponse
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

class RegisterValidation(forms.Form):
    login = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(min_length=6)

def get_contacts(filename):
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            emails.append(a_contact.split()[1])
    return emails

def render_main(request):
    if request.method == 'GET':
        return render(request,'client-page.html')

def guide(request):
    if request.method == 'GET':
        return render(request,'guide.html')

def buying_subscribition(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.user.is_paid == True:
        return redirect('/main')

    if request.method == 'GET':
        return render(request,'subscribition.html',{'user':request.user})

def success_pay_render(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request,'thanks.html')

def preview_template(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        template = HtmlSend.objects.get(pk=int(id))

        with open(f'{template.our_file.url}') as tmp:
            content = tmp.read()
            tmp.close()

        return render(request,'preview.html',{'content':content})

def main(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':

        user = request.user
        all_user_templates = HtmlSend.objects.filter(file_owner = user).all()

        return render(request,'main.html',{'all_user_templates':all_user_templates,'is_paid':request.user.is_paid})

    if request.method == 'POST':
        body = request.POST

        if 'html_file_download' in request.POST:
            our_file = request.FILES['html_file']
            filename = request.POST.get('html_file_download')

            extention = filename[len(filename) - 4: ]

            if extention != 'html':
                messages.add_message(request, messages.ERROR, 'Вы можете загружать только html файлы!')
                return redirect('/main')

            prev_active = HtmlSend.objects.filter(is_active = True).first()
            if prev_active != None:
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


            return redirect('/main')

        if ('template_url' in request.POST) and ('template_id' in request.POST):
            template_id = request.POST.get('template_id')
            template_url = request.POST.get('template_url')

            active_template = HtmlSend.objects.filter(id=int(template_id)).first()
            active_template.is_active = True
            active_template.save()

            user = request.user
            user.active_template = template_url
            user.save()

            return redirect('/main')


        if 'myself' in body:
            if request.user.active_template != None:
                if request.user.emails_amount != 0:
                    email_amount = int(request.user.emails_amount)
                    email_amount -= 1

                    user = request.user
                    user.emails_amount = email_amount
                    user.save()

                    email = body.get('email')
                    subject = body.get('subject')

                    sending_file = request.user.active_template

                    connection = get_connection(username=request.user.mail_username,password=request.user.mail_password,host=request.user.mail_host,port=request.user.mail_port,use_tls=request.user.use_tls,use_ssl=request.user.use_ssl)

                    html_message = render_to_string(f'{sending_file}'[35:])
                    plain_message = strip_tags(html_message)
                    mail.send_mail(subject,plain_message,request.user.mail_username,[email],html_message=html_message,connection=connection)
                    messages.add_message(request, messages.ERROR, 'Отправлено!')
                else:
                    messages.add_message(request, messages.ERROR, 'У вас не осталось email!')
            else:
                messages.add_message(request, messages.ERROR, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

        if 'myself_text' in body:
            if request.user.active_template != None:
                if request.user.emails_amount != 0:
                    email_amount = int(request.user.emails_amount)
                    email_amount -= 1

                    user = request.user
                    user.emails_amount = email_amount
                    user.save()

                    email = body.get('email')
                    subject = body.get('subject')
                    message = body.get('message')

                    connection = get_connection(username=request.user.mail_username,password=request.user.mail_password,host=request.user.mail_host,port=request.user.mail_port,use_tls=request.user.use_tls,use_ssl=request.user.use_ssl)

                    mail.send_mail(subject,message,request.user.mail_username,[email],connection=connection)
                    messages.add_message(request, messages.ERROR, 'Отправлено!')
                else:
                    messages.add_message(request, messages.ERROR, 'У вас не осталось email!')
            else:
                messages.add_message(request, messages.ERROR, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

        if 'sending_from_txt_text' in body:
            subject = body.get('subject')
            message = body.get('message')

            email_txt_filename = request.POST.get('email_txt_filename_text')
            if email_txt_filename != 'txt':
                messages.add_message(request, messages.ERROR, 'Вы можете загружать только txt')
                return redirect('/main')

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

                for email in emails:
                    if request.user.emails_amount != 0:
                        email_amount = int(request.user.emails_amount)
                        email_amount -= 1

                        user = request.user
                        user.emails_amount = email_amount
                        user.save()
                        mail.send_mail(subject,message,request.user.mail_username,[email],connection=connection)
                        messages.add_message(request, messages.ERROR, 'Отправлено!')

                    else:
                        messages.add_message(request, messages.ERROR, 'У вас нет emails!')

                file_to_parse.delete()
            else:
                messages.add_message(request, messages.ERROR, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

        if 'sending_from_txt' in body:
            subject = body.get('subject')

            email_txt_filename = request.POST.get('email_txt_filename')
            if email_txt_filename != 'txt':
                messages.add_message(request, messages.ERROR, 'Вы можете загружать только txt')
                return redirect('/main')

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

                html_message = render_to_string(f'{sending_file}'[35:])
                plain_message = strip_tags(html_message)
                for email in emails:
                    if request.user.emails_amount != 0:
                        email_amount = int(request.user.emails_amount)
                        email_amount -= 1



                        user = request.user
                        user.emails_amount = email_amount
                        user.save()
                        mail.send_mail(subject,plain_message,request.user.mail_username,[email],html_message=html_message,connection=connection)
                        messages.add_message(request, messages.ERROR, 'Отправлено!')

                    else:
                        messages.add_message(request, messages.ERROR, 'У вас нет emails!')

                file_to_parse.delete()
            else:
                messages.add_message(request, messages.ERROR, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

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
            messages.add_message(request, messages.ERROR, 'Email конфигурация изменена!')

            return redirect('/main')

        if 'one_number_send' in body:
            phone_number = body.get('phone_number')
            message_body = body.get('one_message_body')

            account_sid = request.user.twilio_account_sid
            auth_token = request.user.twilio_auth_token
            from_who_send = request.user.twilio_phone_number

            if request.user.messages_amount != 0:
                messages_amount = int(request.user.messages_amount)
                messages_amount -= 1

                user = request.user
                user.messages_amount = messages_amount
                user.save()

                client = Client(account_sid, auth_token)
                message = client.messages \
                    .create(
                        body=message_body,
                        from_=from_who_send,
                        to=phone_number,

                    )
                messages.add_message(request, messages.ERROR, 'Отправлено!')
            else:
                messages.add_message(request, messages.ERROR, 'У вас не осталось SMS!')

            return redirect('/main')

        if 'txt_number_send' in body:

            sms_txt_filename = request.POST.get('sms_txt_filename')

            if sms_txt_filename != 'txt':
                messages.add_message(request, messages.ERROR, 'Вы можете загружать только txt')
                return redirect('/main')

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
                if request.user.messages_amount != 0:
                    messages_amount = int(request.user.messages_amount)
                    messages_amount -= 1

                    user = request.user
                    user.messages_amount = messages_amount
                    user.save()
                    message = client.messages \
                        .create(
                            body=message_body,
                            from_=from_who_send,
                            to=number
                        )
                else:
                    messages.add_message(request, messages.ERROR, 'У вас не осталось SMS!')
            messages.add_message(request, messages.ERROR, 'Отправлено!')
            file_to_parse.delete()

            return redirect('/main')

        if 'twilio_config' in body:
            twilio_number = body.get('twilio_number')
            twilio_account_sid = body.get('twilio_sid')
            twilio_auth_token = body.get('twilio_token')

            user = request.user
            user.twilio_account_sid = twilio_account_sid
            user.twilio_auth_token = twilio_auth_token
            user.twilio_phone_number = twilio_number
            user.save()
            messages.add_message(request, messages.ERROR, 'Twilio конфигурация изменена!')
            return redirect('/main')




def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):
    if request.method == 'GET':
        return render(request,'register.html')

    if request.method == 'POST':
        username = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username = username).exists():
                messages.add_message(request, messages.ERROR, 'Пользователь с таким именем уже существует!')
                return redirect('/register')
        else:
            form = RegisterValidation(request.POST)
            if not form.is_valid():
                return HttpResponse('Заполните все поля!')

            user = CustomUser()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()

            login(request, user)
            return redirect('/main')

def login_page(request):
    if request.method == 'GET':
        return render(request,'login.html')

    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():

            messages.add_message(request, messages.ERROR, 'Данные неверны!')
            return redirect('/login')

        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)


        if user is None:
            messages.add_message(request, messages.ERROR, 'Данные неверны!')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/')
