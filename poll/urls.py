from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # url(r'^index/(?P<page>[0-9]+)/$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^ques/$', views.ques, name='ques'),
    url(r'^ques/(?P<question_id>[0-9]+)/$', views.ques, name='ques'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.logout, name='logout')
]