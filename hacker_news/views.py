<<<<<<< HEAD
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response
from django.template import RequestContext
from django.views.generic import ListView

from hacker_news.models import New, comment

from .forms import CommentForm, NewsUploadForm


class NewsListView(ListView):
    template_name = 'hacker-news/news.html'
    context_object_name = 'news'

    def get(self, request, *args, **kwargs):
        queryset = New.objects.order_by('-post_date')
        context = locals()
        context[self.context_object_name] = queryset
        return render_to_response(self.template_name, context, context_instance=RequestContext(request))

def news_detail(request, id=None):
    instance = get_object_or_404(New, id = id)
    form = CommentForm(request.POST or None)
    reply = CommentForm(request.POST or None)
    if 'Comment' in request.POST:
        if form.is_valid():
            form_obj = comment(text=request.POST.get('text'), link = instance, comment_link=None)
            form_obj.save()
            return HttpResponseRedirect(reverse('hacker-news:news_detail', kwargs={'id': id}))
    else:
        if reply.is_valid():
            comment_instance = get_object_or_404(comment, id = request.POST.get('comment_id'))
            form_obj = comment(text=request.POST.get('text'), link = instance, comment_link= comment_instance)
            form_obj.save()
            return HttpResponseRedirect(reverse('hacker-news:news_detail', kwargs={'id': id}))
    comments = instance.comment_set.filter(comment_link=None)
    reply_comments = instance.comment_set.filter(comment_link__isnull=False)

    context = {
        'news': instance,
        'comments': comments,
        'form': form,
        'reply': reply,
        'reply_comments': reply_comments,
    }
    return render(request, 'hacker-news/news_detail.html', context) 

def vote_update(request, id=None):
    instance = get_object_or_404(New, id = id)
    instance.upvotes += 1
    instance.save()
    return HttpResponseRedirect(reverse('hacker-news:news_list'))


def register(request):
    return render(request, 'hacker-news/register.html')

def login(request):
    return render(request, 'hacker-news/login.html')

def upload(request):
    form = NewsUploadForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False) 
        instance.save()
        return HttpResponseRedirect(reverse('hacker-news:news_list'))
    context = {
        "form": form,
    }
    return render(request, "hacker-news/news_upload.html", context)
=======
from django.shortcuts import render
from django.views.generic import ListView

from hacker_news.models import News


class NewsListView(ListView):
    queryset = News.objects.order_by("-date")[:10]
    template_name = 'hacker-news/news.html'
    context_object_name = 'news'
<<<<<<< HEAD
>>>>>>> 125bce7... First commit hacker-news
=======

def register(request):
    return render(request, 'hacker-news/register.html')

def login(request):
    return render(request, 'hacker-news/login.html')

>>>>>>> c143006... Added some static files and urlpatterns
