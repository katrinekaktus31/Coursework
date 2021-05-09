from django.contrib.auth.models import User
# from django.db import models
from django.contrib.gis.db import models


# Create your models here.
class Earthquake(models.Model):
    earthquake_id = models.BigAutoField(primary_key=True)
    geography = models.PointField(geography=True)
    datetime = models.DateTimeField()
    place = models.CharField(max_length=128)
    mag = models.FloatField()

    def __str__(self):
        return self.place

class Article(models.Model):
    article_id = models.BigAutoField(primary_key=True)
    fk_earthquake_id = models.ForeignKey(Earthquake, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    public_datetime = models.DateTimeField()
    article_content = models.TextField()
    url = models.TextField()

    def __str__(self):
        return self.title
