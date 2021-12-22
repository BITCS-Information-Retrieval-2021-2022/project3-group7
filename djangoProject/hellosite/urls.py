from django.urls import path,re_path
from hellosite import views
from hellosite.views import *
app_name="hellosite"
urlpatterns = [
    path('', views.hello, name='hello'),
    path('search',views.search,name='search'),
    re_path(r'^display',views.display,name='display'),
    # path('graph',views.graph,name='display'),
    path(r'graph/<int:ID>', graph)
]