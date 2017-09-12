from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse
import sys

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)

    # It's one way to build a "full" URL, including the domain name and the http(s) part
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n<a href="/" target="_blank">{url}</a>'
    send_mail('Your login link for Superlists',
              message_body,
              '550906133@qq.com',
              [email],
              )
    messages.add_message(
        request,
        messages.SUCCESS,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

def login(request):
    user = auth.authenticate(uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
