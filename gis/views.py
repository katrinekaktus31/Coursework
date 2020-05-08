from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    # return HttpResponse("Hello world")
    return render(request, 'gis/home.html')


def about(request):
    return render(request, 'gis/about.html')


def add_layer(request):
    return render(request, 'gis/add_layer.html')
