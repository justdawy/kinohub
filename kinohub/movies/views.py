from django.shortcuts import render
from django.db.models import Prefetch

from movies.models import Movie, Category

def index(request):
    categories = Category.objects.prefetch_related(
        Prefetch(
            "movies",
            queryset=Movie.objects.order_by("-created_on")
        )
    )
    context = {"categories": categories}
    return render(request, 'movies/index.html', context=context)
