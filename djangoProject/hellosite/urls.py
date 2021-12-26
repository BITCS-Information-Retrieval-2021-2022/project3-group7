from django.urls import path,re_path
from hellosite import views
from hellosite.views import *
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.views.generic.base import TemplateView
from django.http import HttpResponse
app_name="hellosite"
urlpatterns = [
    path('', views.search, name='search'),
    path('search',views.search,name='search'),
    re_path(r'^display',views.display,name='display'),
    # path('graph',views.graph,name='display'),
    path(r'graph/<str:sid>', views.graph,name="graph"),
    url('sub',views.sub,name='sub')
]