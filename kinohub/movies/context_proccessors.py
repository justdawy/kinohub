from django.conf import settings
from django.core.cache import cache
from django.db.models import Prefetch

from .models import Category, Movie


def global_vars(request):
    cache_key = "categories"
    categories = cache.get(cache_key)

    if not categories:
        movies = Prefetch(
            "movies",
            queryset=Movie.objects.all().order_by("-created_on")[:8],
            to_attr="first_movies",
        )
        categories = (
            Category.objects.prefetch_related(movies)
            .filter(is_visible_on_home=True)
            .order_by("position")
        )
        cache.set(cache_key, categories, timeout=300)

    return {
        "site_name": settings.SITE_NAME,
        "categories": categories,
    }
