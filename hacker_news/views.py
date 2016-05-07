from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.template import RequestContext
from django.views.generic import ListView
from django.conf import settings
from django.views.generic import ListView
from flask.views import View

from django.contrib import auth
from django.contrib.auth.models import User, Group
from hacker_news.models import News, UserProfile
from oauth.authorization import Authorization
from oauth.exceptions import OAuthError
from oauth.request import UserFieldAPIRequest

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

class NewsListView(ListView):
    queryset = News.objects.order_by("-date")[:10]
    template_name = 'hacker-news/news.html'
    context_object_name = 'news'

class SSOAuthorizationView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.GET.get('next') != '' and request.GET.get('next') is not None:
                return redirect(request.GET.get('next'))
            else:
                return redirect(settings.LOGIN_REDIRECT_URL)
        try:
            token = Authorization(request).get_token()
        except OAuthError as e:
            return render(request, 'hacker-news/login.html', {'error': e.message, 'client_id': settings.CLIENT_ID})

        if not token:
            return render(request, 'hacker-news/login.html', {'client_id': settings.CLIENT_ID})

        user_obj = UserFieldAPIRequest(
            fields=[
                'id',
                'first_name',
                'last_name',
                'email',
                'username',
            ],
            access_token=token.access_token,
        ).get_oauth_user()

        user, created = User.objects.get_or_create(username=user_obj.username)  # type: Tuple[User, bool]
        user.set_unusable_password()

        user.first_name = user_obj.first_name
        user.last_name = user_obj.last_name
        user.email = user_obj.email
        user.is_staff = True
        user.save()

        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.nickname = user_obj.username
        user_profile.save()

        group = Group.objects.get(name__iexact='Content Developer')
        group.user_set.add(user)

        user.backend = 'django.contrib.auth.backends.ModelBackend'
        auth.login(request, user)

        if request.GET.get('state') != '' and request.GET.get('state') is not None:
            return redirect(request.GET.get('state'))
        else:
            return redirect(settings.LOGIN_REDIRECT_URL)

