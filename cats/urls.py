from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signout/', views.signout, name='signout'),
    url(r'^likes/$', views.LikesView.as_view(), name='likes'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^more/$', views.MoreView.as_view(), name='more'),
]

