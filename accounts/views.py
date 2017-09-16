from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from accounts.models import Token
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
import sys

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    token = Token.objects.create(email=email)

    # It's one way to build a "full" URL, including the domain name and the http(s) part
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    subject = 'Your login link for Superlists'
    text_content = 'Use this link to log in:\n\n'
    from_email = '550906133@qq.com'
    html_content = f'<html><body><h3>Use this link to log in:</h3><br><br><a href="{url}">{url}</a></body></html>'
    msg = EmailMultiAlternatives(
        subject,
        text_content,
        from_email,
        [email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

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
