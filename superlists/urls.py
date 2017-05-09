"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from lists.views import home_page
from lists.views import view_list
from lists.views import new_list
from lists.views import register_view
from lists.views import register_test, active_user, login, index, logout, blog

app_name='lists'

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^wanderlist/', home_page),
    url(r'^blog/', blog),
    url(r'^lists/', include('lists.urls', namespace="lists")),
    url(r'^register/', register_test),
    url(r'^activate/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', active_user),
    url(r'^$', login),
    url(r'^index/', index),
    url(r'^logout/', logout)
    # 参数 token 通过正则匹配传到 active_user(request, token) 中

]
