from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return HttpResponse('index')
    #return render(request, 'cats/index.html', {})

def signin(request):
    error = ''
    return HttpResponse('signin')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect(request.GET.get('next') or reverse('cats:home'))
        else:
            # Return an 'invalid login' error message.
            error = '用户名或密码错误'

    return render(request, 'cats/login.html', {"error": error})

def signout(request):
    return HttpResponse('logout')
    logout(request)
    return HttpResponseRedirect(reverse('wages:index'))
