from django.views.generic.base import View,TemplateView,RedirectView
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json

from . import models as Cat_models
from .forms import SigninForm,SuggestForm
# Create your views here.

class IndexView(TemplateView):
    template_name = 'cats/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        imgs = Cat_models.CatImgs.objects.with_info(0, 20)
        context['imgs'] = imgs
        context['title'] = 'Emmmmmm'
        return context

class SigninView(View):
    form_class = SigninForm
    initial = {'title': '登录'}
    template_name = 'cats/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')

def signout(request):
    logout(request)

class suggestView(View):
    form_class = SigninForm
    initial = {'title': '登录'}
    template_name = 'cats/signin.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')


class LikesView(View):
    def post(self, request, *args, **kwargs):
        return HttpResponse(json.dumps({'status':'0', 'content':'Hello, World!', 'code': 0}))

class CommentView(View):

    def get(self, request, *args, **kwargs):
        img_id = int(request.GET['id']) if 'id' in request.GET else 0
        if img_id > 0:
            is_comment = Cat_models.CatImgs.objects.get(id=img_id).comments.user_comment.filter(author='carl')
        else:
            return Http404('Not Found')

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
        n = int(kwargs['n'])
        context['list'] = Cat_models.CatImgs.objects.with_info(n, 30)
        return context
