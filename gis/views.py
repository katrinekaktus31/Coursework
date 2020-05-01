from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    # return HttpResponse("Hello world")
    return render(request, 'gis/home.html')


def about(request):
    return render(request, 'gis/about.html')


def gis_online(request):
    return render(request, 'gis/gis_online.html')
