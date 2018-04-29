from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^logout$', views.logout),
    url(r'^login$', views.login),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^quote$', views.quote),
    url(r'^fave/(?P<qid>\d+)$', views.fave),
    url(r'^unfave/(?P<qid>\d+)$', views.unfave),
    url(r'^userquotes/(?P<uid>\d+)$', views.userQuotes),
]
