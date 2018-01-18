from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^result', views.GetResult.as_view(), name='get'),
]
