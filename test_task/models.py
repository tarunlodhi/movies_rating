from django.db import models

class Movies(models.Model):
    tconst = models.CharField(max_length=20, primary_key=True)
    titleType = models.CharField(max_length=100)
    primaryTitle = models.CharField(max_length=255)
    runtimeMinutes = models.IntegerField()
    genres = models.CharField(max_length=255)
    averageRating = models.FloatField(default=0.0)  # Add this field

    def __str__(self):
        return self.primaryTitle

class Ratings(models.Model):
    tconst = models.CharField(max_length=20, primary_key=True)
    averageRating = models.FloatField()
    numVotes = models.IntegerField()
