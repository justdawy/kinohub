from django.conf import settings
from django.core.paginator import Paginator
from django.views import generic

from movies.models import Category, Genre, Movie


class IndexView(generic.TemplateView):
    template_name = "movies/index.html"


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "movie_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players_list = []
        if self.object.category.name == "Фільми":
            for player in self.object.players.all():
                for player_item in player.items.all():
                    players_list.append(
                        {
                            "title": player_item.player.title,
                            "file": settings.PROXY_URL + player_item.url,
                        }
                    )
            context["players_list"] = players_list
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "movies/category_view.html"
    slug_field = "slug"
    slug_url_kwarg = "category_slug"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.get_movies()
        context["genres"] = Genre.objects.all()
        context["movies"] = movies
        context["page_obj"] = movies
        return context

    def get_movies(self):
        queryset = self.object.movies.all()
        paginator = Paginator(queryset, 30)  # paginate_by
        page = self.request.GET.get("page")
        movies = paginator.get_page(page)
        return movies
