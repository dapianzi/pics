from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/', views.signin, name='login'),
    url(r'^signout/', views.signout, name='logout'),
    url(r'^likes/$', views.likes, name='sendingmail'),
    url(r'^delete/$', views.delete, name='ajaxsendmail'),
    url(r'^more/$', views.more, name='resetpassword'),
]

