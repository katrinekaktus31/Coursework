"""GISDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
import gis.views

urlpatterns = [
    url(r'^$', gis.views.home, name='home'),
    url(r'^home', gis.views.home, name='home'),
    url(r'^earthquaks2', gis.views.earthquaks2, name='earthquaks2'),
    url(r'^earthqueaks', gis.views.earthqueaks, name='earthqueaks'),
    url(r'^add_layer', gis.views.add_layer, name='add_layer'),
    url(r'^about/$', gis.views.about, name='about'),
    url(r'^article/$', gis.views.article, name='article'),
]
