from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django import forms
from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.contrib import messages
from django.db.models import Q

import hashlib,hmac

from django.core.mail import send_mail,get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail

from .models import *

from time import time as t
import time

import json

import requests
from bs4 import BeautifulSoup as bs
import csv

import random

from time import sleep as sp


def getFormSignature(account,summ,desc='Пополнение баланса',secretKey='03f4af025c8e4e1d54a26e6c5a8a00dc'):
    hashStr = account + '{up}' + desc + '{up}' + str(summ) + '{up}' + secretKey
    res = hashlib.sha256(hashStr.encode('utf-8')).hexdigest()
    return res

def e_handler404(request,exception):
    return render(request,'404.html')
 
def e_handler500(request):
    return redirect(request,'500.html')

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
            emails.append(a_contact.split()[0])
    return emails

def render_main(request):
    if request.method == 'GET':
        return render(request,'client-page.html')

    if request.method == 'POST':
        email = request.POST.get('mailer-test','')

        if email != '':
            connection = get_connection(username="mailer-help@list.ru",password='sashket2003',host='smtp.mail.ru',port=465,use_tls=False,use_ssl=True)
            mail.send_mail('Mailer','Это тестовое письмо пришло с Mailer!','mailer-help@list.ru',[email],connection=connection)
            messages.add_message(request, messages.ERROR, 'Проверьте вашу почту!')
            return redirect('/')
        else:
            messages.add_message(request, messages.SUCCESS, 'Произошла неизвестная ошибка!')
            return redirect('/')
            
def request_check(request):

    status = request.GET.get('method')
    user = request.GET.get('params[account]')
    summ = request.GET.get('params[payerSum]')
    id = request.GET.get('params[unitpayId]')

    if not Transaction.objects.filter(status = id).exists:
        trans = Transaction()
        trans.account = user
        trans.summ = summ
        trans.status = id
        trans.save()
    else:
        return JsonResponse({"error": {"message": "Неожиданный сбой в матрице,Нео уже в пути!"}})

    user_in_sys = CustomUser.objects.filter(username=user).first()

    if status == 'error':
        return JsonResponse({"error": {"message": "Неожиданный сбой в матрице,Нео уже в пути!"}})

    if status == 'check':
        if Transaction.objects.filter(status = id).exists():
            return JsonResponse({"result": {"message": "Запрос успешно обработан"}})
        else:
            return JsonResponse({"error": {"message": "Неожиданный сбой в матрице,Нео уже в пути!"}})
            

    if status == 'pay':
        user_in_sys.balance = summ
        user_in_sys.save()

        return JsonResponse({"result": {"message": "Запрос успешно обработан"}})

def guide(request):
    if request.method == 'GET':
        balance = "%.2f" % (request.user.balance)
        guides = GuideArticle.objects.all()
        return render(request,'guide.html',{'balance':balance,'guides':guides})

def editor(request):
    if not request.user.is_authenticated:        
        return redirect('/login')

    if request.method == 'GET':
        return render(request,'editor.html')

    if request.method == 'POST':
        code_template = request.POST.get('code_of_template','')
        filename = request.POST.get('filename','')
        if code_template == '' or filename == '':
            messages.add_message(request, messages.SUCCESS, 'Произошла неизвестная ошибка,попробуйте позже!')
            return redirect('/editor')

        try:
            filename = filename.split('.')[0] + str(int(t() * 1000))
        except:
            filename = filename + str(int(t() * 1000))


        with open(f'mail/templates/sending-templates/{filename}.html','a') as f:
            f.write(code_template)
            f.close()


        prev_active = HtmlSend.objects.filter(is_active = True).first()
        if prev_active != None:
            prev_active.is_active = False
            prev_active.save()

        prev_active = HtmlSendFromConstructor.objects.filter(is_active = True).first()
        if prev_active != None:
            prev_active.is_active = False
            prev_active.save()
            

        const_file = HtmlSendFromConstructor()
        const_file.filename = filename + '.html'
        const_file.url = f'mail/templates/sending-templates/{filename}.html'
        const_file.file_owner = request.user
        const_file.is_active = True
        const_file.save()

        user = request.user
        user.active_template = const_file.url
        user.save()

        messages.add_message(request, messages.ERROR, 'Ваш файл успешно сохранен!')
        return redirect('/main')

def buying_subscribition(request):
    if not request.user.is_authenticated:        
        return redirect('/login')

    if request.method == 'GET':
        balance = "%.2f" % (request.user.balance)
        return render(request,'subscribition.html',{'user':request.user,'balance':balance})

    if request.method == 'POST':
        if 'constructor_sum' in request.POST:
            summa = request.POST.get('constructor_sum','')
            if summa == '' or summa == '0':
                messages.add_message(request, messages.SUCCESS, 'Что-то пошло не так!')
                return redirect('/buy_subscribe')
            else:
                if request.user.balance >= float(summa):
                    emails = int(request.POST.get('email_amount'))
                    avitos = int(request.POST.get('avito_amount'))
                    tius = int(request.POST.get('tiu_amount'))
                    avg_amount = int(request.POST.get('avg_price_amount'))
                    templates_amount = int(request.POST.get('templates_amount'))

                    user = request.user
                    user.balance -= float(summa)
                    user.emails_amount += emails
                    user.parse_tiu_amount += tius
                    user.parse_avito_amount += avitos
                    user.average_sum_amount += avg_amount
                    user.templates_amount += templates_amount 
                    user.save()

                    messages.add_message(request, messages.ERROR, 'Покупка успешно совершена!')
                    return redirect('/buy_subscribe')
                else:
                    messages.add_message(request, messages.SUCCESS, 'На вашем счете недостаточно средств!')
                    return redirect('/buy_subscribe')

        if 'sells_2.0' in request.POST:
            if request.user.balance >= 25999:

                user = request.user
                user.balance -= 25999
                user.emails_amount += 100000
                user.parse_tiu_amount += 30000
                user.parse_avito_amount += 25000
                user.templates_amount += 50
                user.average_sum_amount += 15 
                user.save()

                messages.add_message(request, messages.ERROR, 'Покупка успешно совершена!')
                return redirect('/buy_subscribe')
            else:
                messages.add_message(request, messages.SUCCESS, 'На вашем счете недостаточно средств!')
                return redirect('/buy_subscribe')

        if 'sell_of_the_year' in request.POST:
            if request.user.balance >= 22999:

                user = request.user
                user.balance -= 22999
                user.emails_amount += 70000
                user.parse_tiu_amount += 15000
                user.parse_avito_amount += 20000
                user.templates_amount += 20
                user.average_sum_amount += 10 
                user.save()

                messages.add_message(request, messages.ERROR, 'Покупка успешно совершена!')
                return redirect('/buy_subscribe')
            else:
                messages.add_message(request, messages.SUCCESS, 'На вашем счете недостаточно средств!')
                return redirect('/buy_subscribe')

        if 'conversy_plus' in request.POST:
            if request.user.balance >= 17599:
            
                user = request.user
                user.balance -= 15599
                user.emails_amount += 30000
                user.parse_tiu_amount += 15000
                user.templates_amount += 10
                user.average_sum_amount += 15 
                user.save()

                messages.add_message(request, messages.ERROR, 'Покупка успешно совершена!')
                return redirect('/buy_subscribe')
            else:
                messages.add_message(request, messages.SUCCESS, 'На вашем счете недостаточно средств!')
                return redirect('/buy_subscribe')

def success_pay_render(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request,'thanks.html')

def fail_pay_render(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render(request,'fail.html')

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

def preview_template_from_constructor(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if request.method == 'GET':
        id = request.GET.get('id')
        template = HtmlSendFromConstructor.objects.get(pk=int(id))

        with open(f'{template.url}') as tmp:
            content = tmp.read()
            tmp.close()

        return render(request,'preview.html',{'content':content})
    
def main(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    
    if request.method == 'GET':
        
        user = request.user
        all_user_templates = HtmlSend.objects.filter(file_owner = user).order_by('-id')
        
        all_user_templates_from_constructor = HtmlSendFromConstructor.objects.filter(file_owner = user).order_by('-id')

        all_user_parses = ClientParsing.objects.filter(file_owner=request.user.username).order_by('-id')
        all_length = len(all_user_parses)

        balance = "%.2f" % (request.user.balance)

        return render(request,'main.html',{'all_user_templates':all_user_templates,'all_user_templates_from_constructor':all_user_templates_from_constructor,'all_user_parses':all_user_parses,'parse_length':all_length,'balance':balance})

    if request.method == 'POST':
        try:
            body_unicode = request.body.decode('utf-8')
            body = json.loads(body_unicode)
        except:
            body = request.POST

        if 'html_file_download' in body and not 'parse-tiu' in body:
          if request.user.templates_amount > 0:
            our_file = request.FILES['html_file']
            filename = request.POST.get('html_file_download')

            extention = filename[len(filename) - 4: ]

            if extention != 'html':
                messages.add_message(request, messages.SUCCESS, 'Вы можете загружать только html файлы!')
                return redirect('/main')

            prev_active = HtmlSend.objects.filter(is_active = True).first()
            if prev_active != None:
                prev_active.is_active = False
                prev_active.save()
                
            prev_active = HtmlSendFromConstructor.objects.filter(is_active = True).first()
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

          else:
              messages.add_message(request, messages.SUCCESS, 'У вас не осталось шаблонов для загрузки!')
              return redirect('/main')

        if ('template_url' in body) and ('template_id' in body):
            template_id = request.POST.get('template_id')
            template_url = request.POST.get('template_url')

            active_template = HtmlSend.objects.filter(id=int(template_id)).first()
            active_template.is_active = True
            active_template.save()

            user = request.user
            user.active_template = template_url
            user.save()

            return redirect('/main')

        if ('template_construct_url' in body) and ('template_construct_id' in body):
            template_id = request.POST.get('template_construct_id')
            template_url = request.POST.get('template_construct_url')

            active_template = HtmlSendFromConstructor.objects.filter(id=int(template_id)).first()
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

                    try:
                        html_message = render_to_string(f'{sending_file}'[15:])
                        plain_message = strip_tags(html_message)
                        mail.send_mail(subject,plain_message,request.user.mail_username,[email],html_message=html_message,connection=connection)
                        messages.add_message(request, messages.ERROR, 'Отправлено!')

                        user = request.user
                        sent_amount = user.sent
                        sent_amount += 1
                        user.sent = sent_amount
                        user.save()
                    
                    except:
                        email_amount = int(request.user.emails_amount)
                        email_amount += 1

                        user = request.user
                        user.emails_amount = email_amount
                        unsent_amount = user.unsent
                        unsent_amount += 1
                        user.unsent = unsent_amount
                        user.save()

                        messages.add_message(request, messages.SUCCESS, 'Не отправлено!')
                        
                else:
                    messages.add_message(request, messages.SUCCESS, 'У вас не осталось email!')
            else:
                messages.add_message(request, messages.SUCCESS, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

        if 'myself_text' in body:
            if request.user.active_template != None:
                if request.user.emails_amount != 0:
                    email_amount = int(request.user.emails_amount)
                    email_amount -= 1

                    user = request.user
                    user.emails_amount = email_amount
                    user.save()

                    try:
                        email = body.get('email')
                        subject = body.get('subject')
                        message = body.get('message')

                        connection = get_connection(username=request.user.mail_username,password=request.user.mail_password,host=request.user.mail_host,port=request.user.mail_port,use_tls=request.user.use_tls,use_ssl=request.user.use_ssl)

                        mail.send_mail(subject,message,request.user.mail_username,[email],connection=connection)
                        messages.add_message(request, messages.ERROR, 'Отправлено!')

                        user = request.user
                        sent_amount = user.sent
                        sent_amount += 1
                        user.sent = sent_amount
                        user.save()
                   
                    except:
                        email_amount = int(request.user.emails_amount)
                        email_amount += 1

                        messages.add_message(request, messages.SUCCESS, 'Не отправлено!')
                        
                        user = request.user
                        unsent_amount = user.unsent
                        unsent_amount += 1
                        user.unsent = unsent_amount
                        user.emails_amount = email_amount
                        user.save()
                
                else:
                    messages.add_message(request, messages.SUCCESS, 'У вас не осталось email!')
            else:
                messages.add_message(request, messages.SUCCESS, 'Вам нужно выбрать отправляемый шаблон!')
            return redirect('/main')

        if 'sending_from_txt_text' in body:
            subject = body.get('subject')
            message = body.get('message')

            email_txt_filename = request.POST.get('email_txt_filename_text')
            if email_txt_filename != 'txt':
                messages.add_message(request, messages.SUCCESS, 'Вы можете загружать только txt')
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
                        try:
                            mail.send_mail(subject,message,request.user.mail_username,[email],connection=connection)
                            messages.add_message(request, messages.ERROR, 'Отправлено!')
                            user = request.user
                            sent_amount = user.sent
                            sent_amount += 1
                            user.sent = sent_amount
                            user.save()
                        except:
                            email_amount = int(request.user.emails_amount)
                            email_amount += 1

                            messages.add_message(request, messages.SUCCESS, 'Не отправлено!')
                            
                            user = request.user
                            unsent_amount = user.unsent
                            unsent_amount += 1
                            user.unsent = unsent_amount
                            user.emails_amount = email_amount
                            user.save()
                    else:
                        messages.add_message(request, messages.SUCCESS, 'У вас нет emails!')

                file_to_parse.delete()
            else:
                messages.add_message(request, messages.SUCCESS, 'Вам нужно выбрать отправляемый шаблон!')
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
                        try:    
                            mail.send_mail(subject,plain_message,request.user.mail_username,[email],html_message=html_message,connection=connection)
                            messages.add_message(request, messages.ERROR, 'Отправлено!')
                            user = request.user
                            sent_amount = user.sent
                            sent_amount += 1
                            user.sent = sent_amount
                            user.save()
                        except:
                            email_amount = int(request.user.emails_amount)
                            email_amount += 1

                            user = request.user
                            sent_amount = user.sent
                            sent_amount += 1
                            user.sent = sent_amount
                            user.emails_amount = email_amount
                            user.save()

                            messages.add_message(request, messages.SUCCESS, 'Не отправлено!')

                    else:
                        messages.add_message(request, messages.SUCCESS, 'У вас нет emails!')

                file_to_parse.delete()
            else:
                messages.add_message(request, messages.SUCCESS, 'Вам нужно выбрать отправляемый шаблон!')
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

        if 'parse-tiu' in body:
            query = body.get('query','')
            if query == '':
                messages.add_message(request, messages.SUCCESS, 'Заполните поле запроса!')
                return redirect('/main')
            
            HEADERS = {
                'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
                'accept':'*/*'
            }

            def get_html(url):
                r = requests.get(url,headers=HEADERS)
                return r.text

            def get_total_pages(html):
                soup = bs(html,'lxml')
                pages = soup.find('div',class_='x-pager__content').find_all('a',class_='x-pager__item')[-2].text.strip()

                return int(pages)

            def write_csv(data,random_num):
                with open('media/client_databases/tiu_' + str(random_num) + '.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow( (data['title'],data['price'],data['url'],data['phone_number']) )

            def get_page_data(html,random_num):
                soup = bs(html,'lxml')
                ads = soup.find('div',class_='x-catalog-gallery__list').find_all('div',class_='x-gallery-tile')
                
                tiu_amount = request.user.parse_tiu_amount

                for ad in ads:
                    #title,price,url
                    if tiu_amount > 0:
                        try:
                            description = ad.find('div',class_='x-gallery-tile__extra-content')
                            name = description.find('span',class_='ek-text').text.strip().lower()
                            
                            user = request.user
                            am = user.parsed
                            am += 1
                            user.parsed = am
                            user.save()

                        except:
                            user = request.user
                            am = user.unparsed
                            am += 1
                            user.unparsed = am
                            user.save()

                            continue

                        try:
                            title = description.find('span',class_='ek-text').text.strip()
                        except:
                            title = 'Не распарсилось'
                        
                        try:
                            price = description.find('span',class_='x-gallery-tile__price-counter').text.strip()
                        except:
                            price = 'Не распарсилось'

                        try:
                            url = ad.find('a',class_='x-gallery-tile__tile-link').get('href')
                        except:
                            url = 'Не распарсилось'

                        try:
                            phone_number = description.find('span',class_='x-pseudo-link').get('data-pl-main-phone')
                        except:
                            phone_number = 'Не распарсилось'

                        data = {
                            'title':title,
                            'price':price,
                            'url':url,
                            'phone_number':phone_number,
                        }

                        write_csv(data,random_num)
                        tiu_amount -= 1
                        request.user.parse_tiu_amount = tiu_amount
                        request.user.save()

                    else:
                        messages.add_message(request, messages.SUCCESS, 'У вас закончились парсинки!')
                        return redirect('/main')

            def parse_tiu(query):
                random_num = int(t() * 1000)

                url = 'https://tiu.ru/search?page=1&search_term=' + query  
                base_url = 'https://tiu.ru/search?'
                query_url = '&search_term='
                page_url = 'page='

                total_pages = get_total_pages(get_html(url))

                filename = 'tiu_' + str(random_num) + '.csv'
    
                f = open('media/client_databases/' + filename,'a+')
                newParsing = ClientParsing()
                newParsing.filename = filename
                newParsing.file_owner = request.user.username
                newParsing.url = f'media/client_databases/{filename}'
                newParsing.save()
            
                for i in range(1,3):
                    url_gen = base_url + page_url + str(i) + query_url + query 
                    
                    html = get_html(url_gen)
                    get_page_data(html,random_num)

            if request.user.parse_tiu_amount > 0:
                parse_tiu(query)
            else:
                messages.add_message(request, messages.SUCCESS, 'У вас нет парсинок!')
                return redirect('/main')
            
            return redirect('/main')

        if 'parse-avito' in body:
            query = body.get('query')
            if query == '':
                messages.add_message(request, messages.SUCCESS, 'Заполните поле запроса!')
                return redirect('/main')
            
            HEADERS = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
                    'accept': '*/*',
                    'referer':'https://www.avito.ru/rossiya',
                    'connection':'keep-alive',
                    'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,lt;q=0.6'
            }    
    
            def get_html(url):
                r = requests.get(url,headers=HEADERS)
                return r.text

            def get_total_pages(html):
                soup = bs(html,'lxml')
                pages = soup.find('div',class_='pagination-root-2oCjZ').find_all('span',class_='pagination-item-1WyVp')[-2].text.strip()
                print(pages)
                return int(pages)

            def write_csv(data,random_num):
                with open('media/client_databases/avito_' + str(random_num) + '.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow( (data['title'],data['price'],data['url']) )

            def get_page_data(html,random_num):
                soup = bs(html,'lxml')
                ads = soup.find('div',class_='snippet-list').find_all('div',class_='item')
                
            
                avito_amount = request.user.parse_avito_amount

                for ad in ads:
                    #title,price,url
                    if avito_amount > 0:
                        try:
                            description = ad.find('div',class_='description')
                            name = description.find('a',class_='snippet-link').text.strip().lower()
                            
                            user = request.user
                            am = user.parsed
                            am += 1
                            user.parsed = am
                            user.save()
                        except:
                            user = request.user
                            am = user.unparsed
                            am += 1
                            user.unparsed = am
                            user.save()
                            continue

                        try:
                            title = description.find('a',class_='snippet-link').text.strip()
                        except:
                            title = 'Не распарсилось'
                        
                        try:
                            price = description.find('span',class_='snippet-price').text.strip()
                        except:
                            price = 'Не распарсилось'
                        
                        try:
                            url = 'https://www.avito.ru' + description.find('a',class_='snippet-link').get('href')
                        except:
                            url = 'Не распарсилось'

                        data = {
                            'title':title,
                            'price':price,
                            'url':url,
                        }

                        write_csv(data,random_num)
                        avito_amount -= 1
                        request.user.parse_avito_amount = avito_amount
                        request.user.save()

                    else:
                        messages.add_message(request, messages.ERROR, 'У вас закончились парсинки!')
                        return redirect('/main')

            def avito_parse(query):
                random_num = int(t() * 1000)

                url = 'https://www.avito.ru/rossiya?q=' + query + '&p=1'
                base_url = 'https://www.avito.ru/rossiya?'
                query_url = 'q='
                page_url = '&p='

                total_pages = get_total_pages(get_html(url))
                filename = 'avito_' + str(random_num) + '.csv'

                f = open('media/client_databases/' + filename,'a+')
                newParsing = ClientParsing()
                newParsing.filename = filename
                newParsing.file_owner = request.user.username
                newParsing.url = f'media/client_databases/{filename}'
                newParsing.save()
                

                for i in range(1, total_pages + 1):
                    if request.user.parse_avito_amount > 0:
                        url_gen = base_url + query_url + query + page_url + str(i)
                        
                        html = get_html(url_gen)
                        get_page_data(html,random_num)
                    else:
                        messages.add_message(request, messages.SUCCESS, 'У вас нет парсинок!')
                        return redirect('/main')         
            if request.user.parse_avito_amount > 0:
                avito_parse(query)
            else:
                messages.add_message(request, messages.SUCCESS, 'У вас нет парсинок!')
                return redirect('/main')

            return redirect('/main')

        if 'add_balance' in body:
            money = body.get('sum')

            signature = getFormSignature(account=request.user.username,summ=money)
            user = request.user
            all_user_templates = HtmlSend.objects.filter(file_owner = user).all()

            return JsonResponse({'signature':signature,'sum':money}) 

        if 'get_average_sum' in body:
            if request.user.average_sum_amount > 0:

                query = body.get('query')

                HEADERS = {
                    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36',
                    'accept': '*/*',
                    'referer':'https://www.avito.ru/rossiya',
                    'connection':'keep-alive',
                    'accept-language':'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,lt;q=0.6'
                }

                arr_of_prices = []
                
                def get_html(url):
                    r = requests.get(url)
                    return r.text

                def get_total_pages(html):
                    soup = bs(html, 'lxml')
                    pages = soup.find('div', class_='pagination-root-2oCjZ')
                    total = pages.find_all('span', class_='pagination-item-1WyVp')[-2].text.strip()
                    return int(total)

                def get_page_data(html):
                    soup = bs(html, 'lxml')
                    ads = soup.find('div', class_='snippet-list').find_all('div', class_='item')

                    for ad in ads:
                        try:
                            description = ad.find('div', class_='description')

                        except:

                            print('Сбой в матрице,но мы продолжим!')
                            continue

                        try:
                            price = description.find('span', class_='snippet-price').text.strip()

                        except:
                            price = None

                        if price != None:
                            try:
                                price = price.split(' ')[0] + price.split(' ')[1]
                                arr_of_prices.append(int(price))
                            except:
                                continue
                    


                url = 'https://www.avito.ru/rossiya?q=' + query + '&p=1'
                base_url = 'https://www.avito.ru/rossiya?'
                query_url = 'q='
                page_url = '&p='

                try:
                    total_pages = get_total_pages(get_html(url))
                except:
                    pass

                try:
                    request.user.average_sum_amount -= 1
                    request.user.save()
                    for i in range(1, 3):
                        url_gen = base_url + query_url + query + page_url + str(i)
                        html = get_html(url_gen)
                        get_page_data(html)
                        sp(2)
                except:
                    raise IndexError

                return JsonResponse({'prices':arr_of_prices})
            else:
                return JsonResponse({'not_enough':None})

def logout_page(request):
    logout(request)
    return redirect('/login')

def register_page(request):
    if request.user.is_authenticated:
        return redirect('/main')


    if request.method == 'GET':
        return render(request,'register.html')

    if request.method == 'POST':
        username = request.POST.get('login')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if CustomUser.objects.filter(username = username).exists():
                messages.add_message(request, messages.SUCCESS, 'Пользователь с таким именем уже существует!')
                return redirect('/register')
        else:
            form = RegisterValidation(request.POST)
            if not form.is_valid():
                messages.add_message(request, messages.SUCCESS, 'Заполните все поля!')
                return redirect('/register')

            user = CustomUser()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()

            login(request, user)
            return redirect('/main')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/main')

    if request.method == 'GET':
        return render(request,'login.html')

    if request.method == 'POST':
        form = LoginValidation(request.POST)
        if not form.is_valid():

            messages.add_message(request, messages.SUCCESS, 'Данные неверны!')
            return redirect('/login')

        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)


        if user is None:
            messages.add_message(request, messages.SUCCESS, 'Данные неверны!')
            return redirect('/login')
        else:
            login(request,user)
            return redirect('/main')

def adding_guide(request):
    if not request.user.is_authenticated:
        return redirect('/login')

    if not request.user.is_admin:
        messages.add_message(request, messages.SUCCESS, 'Вы должны обладать правами администратора!')
        return redirect('/guide')

    if request.method == 'GET':
        return render(request,'adding_gude.html')
    
    if request.method == 'POST':
        name = request.POST.get('subject','')
        text = request.POST.get('guide_text','')

        if name == '' or text == '':
            messages.add_message(request, messages.SUCCESS, 'Заполните все поля корректно!')
            return redirect('/guide')

        if 'image_to_download' in request.FILES:
            image = request.FILES['image_to_download']
            
            article = GuideArticle()
            article.name = name
            article.text = text
            article.image = image
            article.save()

        else:
           messages.add_message(request, messages.SUCCESS, 'Вы не загрузили файл!')
           return redirect('/guide')

        messages.add_message(request, messages.ERROR, 'Статья успешно добавлена!')
        return redirect('/guide')
