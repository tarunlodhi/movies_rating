from rest_framework import serializers
from .models import Movies, Ratings

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('tconst', 'titleType', 'primaryTitle', 'runtimeMinutes', 'genres')

class TopRatedMoviesSerializer(serializers.ModelSerializer):
    averageRating = serializers.SerializerMethodField()

    class Meta:
        model = Movies
        fields = ('tconst', 'primaryTitle', 'genres', 'averageRating')

    def get_averageRating(self, obj):
        try:
            rating = Ratings.objects.get(tconst=obj.tconst)
            return rating.averageRating
        except Ratings.DoesNotExist:
            return None
