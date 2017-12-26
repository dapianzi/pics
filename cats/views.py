from django.shortcuts import render
from django.http import HttpResponse
from .controllers import indexController
# Create your views here.

def index(request):
    #return render(request, 'cats/index.html')
    return indexController.index(request)

def signin(request):
    return indexController.signin(request)

def signout(request):
    return indexController.signout(request)

def likes(request):
    pass
def delete(request):
    pass
def more(request):
    pass
