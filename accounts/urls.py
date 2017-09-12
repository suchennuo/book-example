from django.conf.urls import url
from accounts import views
from django.contrib.auth.views import logout

"""
参考：https://my.oschina.net/asktao/blog/894442
django url pattern: 4 个参数
regex: url地址；regex不会去匹配GET或POST参数或域名
view: 当正则表达式匹配到某个条目时，自动将封装的HttpRequest对象作为第一个参数，
正则表达式“捕获”到的值作为第二个参数，传递给该条目指定的视图。
如果是简单捕获，那么捕获值将作为一个位置参数进行传递，如果是命名捕获，那么将作为关键字参数进行传递。
kwargs：任意数量的关键字参数可以作为一个字典传递给目标视图。
name：
对你的URL进行命名，可以让你能够在Django的任意处，尤其是模板内显式地引用它。
相当于给URL取了个全局变量名，你只需要修改这个全局变量的值，在整个Django中引用它的地方也将同样获得改变。
这是极为古老、朴素和有用的设计思想，而且这种思想无处不在。
"""
urlpatterns=[
    url(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    url(r'^login$', views.login, name='login')
]