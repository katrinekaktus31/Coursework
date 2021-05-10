from django.http import HttpResponse
from django.shortcuts import render
from .models import Article


# Create your views here.
def home(request):
    # return HttpResponse("Hello world")
    return render(request, 'gis/home.html')


def about(request):
    return render(request, 'gis/about.html')


def add_layer(request):
    return render(request, 'gis/add_layer.html')


def earthqueaks(request):
    return render(request, 'gis/earthqueaks.html')

#add cors-headers to acces localhost
def earthquaks2(request):
    response = render(request, 'gis/earthquaks2.html', {})
    response["Access-Control-Allow-Origin"] = "http://localhost:8080/"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Allow-Headers"] = "http://127.0.0.1:8000/"
    response['Cache-Control'] = 'no-cache'
    return response

def article(request):
    obj = Article.objects.all()
    context = {
        "obj": obj,
    }
    return render(request, 'gis/article.html', context)