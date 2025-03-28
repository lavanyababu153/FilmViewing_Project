from django.db import models

# Create your models here.

class Genre(models.Model):
    name=models.CharField(max_length=10)
    image=models.ImageField(upload_to="genre",default="sample.jpg")


class Movie(models.Model):
    movie_name = models.CharField(max_length=100)
    movie_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    movie_file = models.FileField(upload_to="Movies")
    movie_poster = models.ImageField(upload_to="Posters")
    director_name = models.CharField(max_length=100)
    duration = models.CharField(max_length=6)
    release_date = models.DateField()
    description = models.TextField(default="no description")
    like_count=models.IntegerField(default=0)
    dislike_count=models.IntegerField(default=0)

    
class Cast(models.Model):
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    role=models.CharField(max_length=100)
    image=models.ImageField(upload_to="Cast")

class Subscription_plan(models.Model):
    name=models.CharField(max_length=50)
    duration_days=models.CharField(max_length=100)
    price=models.IntegerField()
    streaming_quality=models.CharField(max_length=100)
    advertisements=models.CharField(max_length=50)








 
   