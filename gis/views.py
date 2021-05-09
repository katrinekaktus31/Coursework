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

def earthquaks2(request):
    return render(request, 'gis/earthquaks2.html')

def article(request):
    obj = Article.objects.all()
    context = {
        "obj": obj,
    }
    return render(request, 'gis/article.html', context)