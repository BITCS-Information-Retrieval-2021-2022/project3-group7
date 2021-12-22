from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
# Create your views here.
def search(request):
    return render(request, 'begin/search.html')

def hello(request):
    return render(request,'begin/index.html')
    
def display(request):
    m=request.GET['wd']
    # m=m.split(" ")
    type=request.GET['type']
    start=request.GET['start']
    # print(type)
    post={}
    post["type"]="RetrievalPapers"
    post["query"]=m;
    if type:
        post["sortByValue"]=1
    else:
        post["sortByValue"]=0
    post["start"]=start
    total=10
    hit=[]
    hit.append({"Sid":"1","title":"Radio Propagation Characteristics for Short Range Body-Centric Wireless Communications","inCitiationsCount":5,"outCitiationsCount":8})
    hit.append({"Sid":"2","title":"Reduced oxygen tension helps increase the quality of blastocyst available on D5","inCitiationsCount":3,"outCitiationsCount":4})
    hit.append({"Sid":"3","title":"Quasi-static and dynamic mechanical properties of commercial-purity tungsten processed by ECAE at low temperatures","inCitiationsCount":2,"outCitiationsCount":5})
    hit.append({"Sid":"4","title":"Nonlinearities in real exchange rate determination: do African exchange rates follow a random walk?","inCitiationsCount":6,"outCitiationsCount":7})
    hit.append({"Sid":"5","title":"Multiple-point equalization of room impulse response based on the human perception characteristics","inCitiationsCount":8,"outCitiationsCount":3})
    hits={}
    hits["total"]=total
    hits["hit"]=hit
    post["hits"]=hits
    json_post=json.dumps(post)
    # data=json.load(json_post)
    data=post
    return render(request,'begin/display.html',{'total':post["hits"]['total'],'hits':post['hits']['hit'],'query':post['query']})
def graph(request,ID):
    return render(request,'begin/graph.html',{'ID':ID})

