from django.views.generic.base import View,TemplateView,RedirectView
from django.shortcuts import render,redirect,get_object_or_404,get_list_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import json

from django.contrib.auth.models import User
from . import models as Cat_models
from .forms import SigninForm,SuggestForm
# Create your views here.

class IndexView(TemplateView):
    template_name = 'cats/index.html'
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        imgs = Cat_models.CatImgs.objects.with_info(0, 50)
        context['imgs'] = imgs
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
        if not request.user.is_authenticated:
            # Do something for authenticated users.
            return HttpResponse(json.dumps({'status': -1, 'content': 'Invalid user!', 'code': 100}))
        img_id = int(request.POST.get('id', 0))
        user = User.objects.get(username='carl')
        img = Cat_models.CatImgs.objects.get(id=img_id)
        if img:
            pic_like = Cat_models.PicLikes(img=img, user=user, is_like=1)
            pic_like.save()
            return HttpResponse(json.dumps({'status':0, 'content':pic_like.id, 'code': 0}))
        else:
            return HttpResponse(json.dumps({'status':-1, 'content':'Invalid img id!', 'code': 0}))

class CommentView(View):

    def get(self, request, *args, **kwargs):
        img_id = int(request.GET.get('id', 0))
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

class MoreView(View):
    def post(self, request, *args, **kwargs):
        n = request.POST['n']
        result = Cat_models.CatImgs.objects.with_info(int(n), 30)
        content = list()
        for img in result:
            content.append({
                'id': img.id,
                'img_from': img.img_from,
                'img_desc': img.img_desc,
                'n_stars': img.n_stars,
                'n_likes': img.n_likes,
                'n_comments': img.n_comments,
            })
        return HttpResponse(json.dumps({'status':0, 'content':content, 'code': 0}))
