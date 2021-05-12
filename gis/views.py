from django.http import HttpResponse
from django.shortcuts import render
from .models import Article, Earthquake
from django.core import serializers

with open('D:/python_project/PC_project/diploma/GISDjango/gis/static/tableQuake1.geojson', "w",
          encoding="utf-8") as out:
    mast_point = serializers.serialize('geojson', Earthquake.objects.all(),
                                       geometry_field='geography',
                                       fields=('earthquake_id', 'mag', 'place', 'datetime'))
    out.write(mast_point)


# def example(request):
#     objects = Article.objects.filter(fk_earthquake_id=1)
#     with open(r'.static/tableQuake1.geojson', "w") as out:
#         mast_point = serializers.serialize("json", objects)
#         out.write(mast_point)
#     template = loader.get_template('some_template.html')
#     context = {'object': objects}
#     return HttpResponse(template.render(context, request))

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


# add cors-headers to acces localhost
def earthquaks2(request):
    response = render(request, 'gis/earthquaks2.html', {})
    response["Access-Control-Allow-Origin"] = "http://localhost:8080/"
    response["Access-Control-Allow-Methods"] = "GET"
    response["Access-Control-Allow-Headers"] = "http://127.0.0.1:8000/"
    response['Cache-Control'] = 'no-cache'
    return response


def article(request):
    # obj = Article.objects.filter(fk_earthquake_id = 1205)
    obj = Article.objects.filter(fk_earthquake_id_id = 2637)
    context = {
        "obj": obj,
    }
    return render(request, 'gis/article.html', context)
