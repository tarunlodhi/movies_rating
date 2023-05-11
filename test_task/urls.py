from django.urls import path
from .views import *
urlpatterns = [
     path('api/v1/longest-duration-movies', LongestDurationMovies.as_view()),
     path('api/v1/new-movies', NewMovieView.as_view()),
     path('api/v1/top-rated-movies', TopRatedMoviesView.as_view()),
     path('api/v1/genre-movies-with-subtotals', GenreMoviesWithSubtotalsView.as_view()),
     path('api/v1/update-runtime-minutes', UpdateRuntimeMinutesView.as_view()),
]
