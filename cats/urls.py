from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signout/', views.signout, name='signout'),
    url(r'^likes/$', views.likes, name='likes'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^more/$', views.more, name='more'),
]

