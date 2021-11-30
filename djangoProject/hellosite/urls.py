from django.urls import path
from hellosite import views

app_name="hellosite"
urlpatterns = [
    path('', views.hello, name='hello'),
    path('search',views.search,name='search'),
    path(r'^users/$', views.users, name='users'),
]