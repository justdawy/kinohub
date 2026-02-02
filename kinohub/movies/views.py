from django.shortcuts import render
from django.db.models import Prefetch
from django.views import generic

from movies.models import Movie, Category

class IndexView(generic.ListView):
    template_name = "movies/index.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        movies = Prefetch(
            "movies",
            queryset=Movie.objects.all().order_by("-created_on")[:8],
            to_attr="first_movies"
        )
        categories = Category.objects.prefetch_related(movies).filter(
            is_visible_on_home=True).order_by("position")
        return categories

class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "movie_slug"
