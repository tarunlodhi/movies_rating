from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import MovieSerializer,TopRatedMoviesSerializer
from django.db import connection
from .models import Movies ,Ratings

class LongestDurationMovies(APIView):
    def get(self, request, format=None):
        longest_movies = Movies.objects.order_by('-runtimeMinutes')[:10]
        serializer  = MovieSerializer(longest_movies, many=True)
        return Response(serializer.data)

class NewMovieView(APIView):
    def post(self, request):
        try:
            serializer = MovieSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'success'})
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)


class TopRatedMoviesView(APIView):
    def get(self, request):
        top_movies = Ratings.objects.filter(averageRating__gt=6.0).order_by('-averageRating')
        movie_ids = [rating.tconst for rating in top_movies]
        movies = Movies.objects.filter(tconst__in=movie_ids).order_by('-averageRating')
        serialized_movies = TopRatedMoviesSerializer(movies, many=True)
        sorted_movies = sorted(serialized_movies.data, key=lambda x: x['averageRating'], reverse=True)
        return Response(sorted_movies)

class GenreMoviesWithSubtotalsView(APIView):
    def get(self, request):
        try:
            query = """
            SELECT genres, primaryTitle, numVotes
            FROM (
                SELECT m.genres, m.primaryTitle, r.numVotes
                FROM test_task_movies m
                JOIN test_task_ratings r ON m.tconst = r.tconst

                UNION ALL

                SELECT m.genres, 'TOTAL' AS primaryTitle, SUM(r.numVotes) AS numVotes
                FROM test_task_movies m
                JOIN test_task_ratings r ON m.tconst = r.tconst
                GROUP BY m.genres
            ) AS subquery
            WHERE genres IS NOT NULL AND primaryTitle IS NOT NULL
            ORDER BY genres ASC, CASE WHEN primaryTitle = 'TOTAL' THEN 1 ELSE 0 END, primaryTitle ASC
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
                results = cursor.fetchall()
            table = "<table><tr><th>Genre</th><th>Primary Title</th><th>Num Votes</th></tr>"
            for genre, title, num_votes in results:
                if title == "TOTAL":
                    table += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format("", title, num_votes)
                else:
                    table += "<tr><td>{}</td><td>{}</td><td>{}</td></tr>".format(genre, title, num_votes)
            table += "</table>"

            return Response(table)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

class UpdateRuntimeMinutesView(APIView):
    def post(self, request):
        try:
            query = """
            UPDATE test_task_movies
            SET runtimeMinutes =
                CASE
                    WHEN genres = 'Documentary' THEN runtimeMinutes + 15
                    WHEN genres = 'Animation' THEN runtimeMinutes + 30
                    ELSE runtimeMinutes + 45
                END
            """

            with connection.cursor() as cursor:
                cursor.execute(query)
            connection.commit()

            return Response({"message": "Runtime minutes updated successfully."})

        except Exception as e:
            return Response({"error": str(e)}, status=500)