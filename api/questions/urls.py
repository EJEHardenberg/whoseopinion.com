from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

from questions import views

urlpatterns = patterns('',
    url(r'^categories/$', views.CategoryList.as_view(),name='categories'),
    url(r'^category/-1/$', views.get_popular, name='popular'),
    url(r'^category/(?P<category_pk>\d+)/$', views.QuestionList.as_view(),name='questions_for_category'),
    url(r'^(?P<question_pk>\d+)/opinions/$', views.OpinionList.as_view(),name='opinions_for_question'),
    url(r'^auth$',views.get_auth, name='auth')
)

urlpatterns = format_suffix_patterns(urlpatterns)
