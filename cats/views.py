from django.views.generic.base import View,TemplateView,RedirectView
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import cats.models as Cat_models
# Create your views here.

class IndexView(TemplateView):
    template_name = 'cats/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['imgs'] = Cat_models.CatImgs.objects.all()[:15]
        return context

def signin(request):
    return render(request, 'cats/signin.html')

def signout(request):
    logout(request)

class LikesView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

@login_required
def delete(RedirectView):
    def post(self, request, id, *args, **kwargs):
        ImgModel = Cat_models.CatImgs
        img = get_list_or_404(ImgModel, id=id)

class MoreView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(MoreView, self).get_context_data(**kwargs)
        p = int(kwargs['p'])
        context['list'] = Cat_models.CatImgs.objects.all()[(p-1)*5:5]
        return context
