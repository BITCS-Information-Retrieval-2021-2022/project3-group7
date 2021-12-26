from django.shortcuts import render
from django.http import HttpResponse
import json
from .models import User
import requests

# Create your views here.
def search(request):
    return render(request, 'begin/search.html')

def display(request):
    m = request.GET['wd']
    # m=m.split(" ")
    type = request.GET['type']
    start = request.GET['start']
    type=int(type)
    # print(type)
    post = {}
    post["type"] = "RetrievalPapers"
    post["query"] = m
    if type:
        post["sortByValue"] = 1
    else:
        post["sortByValue"] = 0
    post["start"] = start
    if int(start) < 10:
        post["previous"] = 0
    else:
        post["previous"] = int(start) - 10
    post["next"] = int(start) + 10
    r = requests.get(url='http://182.92.1.145:8050/query', params=post)
    data=json.loads(r.text)
    print(data)
    return render(request, 'begin/display.html',
                  {'next': data["next"], "previous": data["previous"], 'type': '0', 'start': data["start"],
                   'total': data["hits"]['total'], 'hits': data['hits']['hit'][int(data["start"]):int(data["start"])+10], 'query': data['query']})



def graph(request,sid):
    post = {}
    post["type"] = "RetrievalNetwork"
    post["query"]=sid
    r = requests.get(url='http://182.92.1.145:8050/networks', params=post)
    data=json.loads(r.text)
    print(type(data))
    print(data)
    res={}
    subgraph = data["subgraph"]
    nodes=subgraph["nodes"]
    res["subgraph"]=subgraph
    for node in nodes:
        res[str(node["id"])]=node
    f = open(
        '/Users/melon/Desktop/Postgraduate/Course/IR/HW/project3-group7/djangoProject/hellosite/templates/begin/sub3.json',
        'w')
    json.dump(res, f)
    f.close()
    return render(request, 'begin/graph.html')

def sub(request):
    f = open(
        '/Users/melon/Desktop/Postgraduate/Course/IR/HW/project3-group7/djangoProject/hellosite/templates/begin/sub3.json',
        'r')
    content = f.read()
    a = json.loads(content)
    print(a["subgraph"].keys())
    return HttpResponse(json.dumps(a), content_type="application/json")
