from django.shortcuts import render
from django.db.models import Prefetch

from movies.models import Movie, Category

def index(request):
    movies = Prefetch(
        "movies",
        queryset=Movie.objects.all().order_by("-created_on")[:8],
        to_attr="first_movies"
    )
    categories = Category.objects.prefetch_related(movies).filter(
        is_visible_on_home=True).order_by("position")
    context = {"categories": categories}
    return render(request, "movies/index.html", context=context)
