from django.shortcuts import render, redirect, render_to_response
from django.http import HttpResponse
from django.contrib import auth
from django.contrib.auth.models import User

from django.template import RequestContext
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import EmailMessage

from lists.models import Item, List

from django.core.exceptions import ValidationError
import logging
import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


from django.conf import settings
import Auth.TokenManager
from Auth.TokenManager import *

from lists.forms import * #ItemForm, ExistingListItemForm, RegisterForm, LoginForm

log = logging.getLogger(__name__)

# Create your views here.
def home_page(request):
    # if request.method == 'POST':
    #     new_item_text = request.POST['text']
    #     Item.objects.create(text=new_item_text)
    #     return redirect('/lists/the-only-list-in-the-world/')

    # items = Item.objects.all()
    # return render(request, 'home.html', {'items':items})
    return render(request, 'home.html', {'form': ItemForm()})
    # else:
    #     new_item_text = ''

    # item = Item();
    # item.text = request.POST.get('text', '')
    # item.save()

    # return render(request, 'home.html',{
    #     # 'new_item_text':request.POST.get('text', ''),
    #     'new_item_text' : new_item_text,
    # })


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    # items = Item.objects.filter(list=list_)
    error = None
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)

    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            # Item.objects.create(text=request.POST['text'], list=list_)

            # form.save(for_list=list_)
            # return redirect(list_)

            form.save()

    return render(request, 'list.html', {'list':list_, "form": form, 'error':error})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        # Item.objects.create(text=request.POST['text'], list=list_)
        form.save(for_list=list_)
        return redirect(list_)
    else:
        return render(request, 'home.html', {"form":form})


# formdef register(request):
#     return render(request, 'login.html', {'form': LoginForm()})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            log.error("email " + email)
        log.error("post for login ")
        return render(request, 'login.html', {'form': LoginForm()})
    else:
        return render(request, 'register.html', {"form": RegisterForm()})


def login(request):
    return render(request, 'home.html', {'form': ItemForm()})

def search_form(request):
    form = ContactForm()
    return render_to_response('search_form.html', {'form':form})

def search(request):
    errors = []
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.data
            # send_email()
            try:
                send_mail("Hi", "This is a test.", settings.EMAIL_HOST_USER, ['550906133@qq.com'], fail_silently=False)
            except SMTPException as e:
                log.error(e)

            return HttpResponseRedirect('/lists/hello/')
            # 何重定向至新的页面，而不是在模板中直接调用render_to_response()来输出 ?
            #  若用户刷新一个包含POST表单的页面，那么请求将会重新发送造成重复
    else:
        form = ContactForm(initial={'subject': 'I love your site!'})
    return render_to_response('search_form.html', {'form': form})


    # if 'q' in request.GET:
    #     message = 'You searched for: %r' % request.GET['q']
    # else:
    #     message = 'You submitted an empty form.'
    # return HttpResponse(message)


def hello(request):
    return HttpResponse("Welcome to %s" % request.path)


def send_simple_email(request):
    send_mail("Hi", "This is a test.", "superlist@yongchaozhang.com", ['550906133@qq.com'])
    return render(request, 'home.html', {'form': ItemForm()})


def send_email(email, token):
    fromaddr = "superlist@yongchaozhang.com"  # prompt("From: ")
    toaddrs = email  # prompt("To: ").split()u
    subject = "Invitation"  # prompt("Subject: ")

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddrs
    msg['Subject'] = subject
    message = "\n".join([u'请访问链接，完成注册:',
                         "/".join(["http://localhost:8000", 'activate', token])])
    msg.attach(MIMEText(message, "plain", "utf-8"))

    server = smtplib.SMTP_SSL(host='smtp.exmail.qq.com', port=465)
    server.set_debuglevel(1)  # 开启调试，会打印调试信息
    print("--- Need Authentication ---")
    server.login('superlist@yongchaozhang.com', 'Tsil@1122')
    server.sendmail(fromaddr, toaddrs, msg.as_string())
    server.quit()


def register_test(request):
    if request.method == 'POST':
        form = RegisterTestForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_active = False
            user.save()
            token = token_confirm.generate_validate_token(username)

            # user = User()
            # user.email = email
            # user.password = password
            # user.username = username
            # user.save()
            # form.save()
            # TODO: Django 默认 username 唯一，当输入相同 username 是 is_valid() == false. 需要修改为以 email 为 key

            print("token %s " % token)
            send_email(email, token)
            return HttpResponse("请登录到注册邮箱中完成验证，有效期为10分钟")
    return render(request, 'register_test.html', {'form': RegisterTestForm()})


def active_user(request, token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        username = token_confirm.remove_validate_token(token)
        users = User.objects.filter(username=username)
        for user in users:
            user.delete()
        return HttpResponse(u'验证链接已经过期，请重新<a href=\"' + django_settings.DOMAIN + u'/\">注册</a>')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("用户不存在")
    user.is_active = True
    user.save()
    return HttpResponse(u'验证成功，请登录<a href=\"' + django_settings.DOMAIN + u'/\">登录</a>')


def login (request):
    if request.method == 'POST':
        # form = LoginForm(request.POST)
        # if form.is_valid():
        # TODO: 为什么 LoginForm is_valid() 一直返回 false ?

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/index/')
    return render(request, 'login.html', {'from' : LoginForm()})

def index(request):
    return render_to_response('index.html', locals())
    # locals() ?

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def blog(request):
    return HttpResponse("Blog")

#TODO: 将用户名与各个APP 关联起来


"""

从用户的请求中读取数据，结合一些定制的逻辑或 URL 中的信息 （list_id),
然后把数据传入表单验证，如果通过就保存数据， 最后重定向或者渲染模板

view 负责模板的重定向和渲染

    之前view 负责读取数据，验证，保存数据，重定向，渲染
    template 负责展示
    典型的 MVC 结构，但 C 模块过于繁重， 拆分出一个 form , 主要负责数据的处理
    包括读取，验证，存入数据库， 设置验证信息。这样，view 模板只负责提供将数据的转移给模板

model 负责数据库中数据的描述
form 负责读取数据，验证，保存数据
template 展示模板

1.  Header information META
        request.META.items()
2.  GET 适合取得数据 和 对应的页面
    POST 利用提交数据更改 DB
3.  request.GET and request.POST 类似字典 request.GET['**']
    eg: if 'user_name' in request.GET:
        return ...
4.  一个页面可能有两种状态，a. 提交过表单了； b. 未提交表单
5.  当表单来源和去向相同的时候， action = "", 也避免硬编码
6.


"""