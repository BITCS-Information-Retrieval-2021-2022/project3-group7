from django.shortcuts import render
from django.http import HttpResponse
from .models import User
# Create your views here.
def search(request):
    return render(request, 'begin/search.html')

def hello(request):
    return render(request,'begin/index.html')

def users(request):
    users=User.objects.order_by("username")
    content={"users":users}
    return render(request,'begin/users.html',content)
