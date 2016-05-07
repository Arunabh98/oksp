from django.conf.urls import url
from hacker_news import views
from hacker_news.views import NewsListView, SSOAuthorizationView

urlpatterns = [
    url(r'^$', NewsListView.as_view(), name='news_list'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^vote-update/(?P<id>\d+)/$', views.vote_update, name='update'),
    url(r'^detail/(?P<id>\d+)/$', views.news_detail, name='news_detail'),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^authorization/$', SSOAuthorizationView.as_view("auth"), name='authorization'),
]
