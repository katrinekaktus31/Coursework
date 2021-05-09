from django.contrib import admin

# Register your models here.
from gis.models import Article, Earthquake

admin.site.register(Article)
admin.site.register(Earthquake)
