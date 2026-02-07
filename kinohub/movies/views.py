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
        if self.object.movie_type == Movie.FILM:
            for player in self.object.players.all():
                for player_item in player.items.all():
                    players_list.append(
                        {
                            "title": player_item.player.title,
                            "file": settings.PROXY_URL + player_item.url,
                        }
                    )
        elif self.object.movie_type == Movie.SERIES:
            for player in self.object.players.all():
                folder = {"title": player.title, "folder": []}
                for player_item in player.items.all():
                    folder["folder"].append(
                        {
                            "title": f"Серія {player_item.episode_number}",
                            "file": settings.PROXY_URL + player_item.url,
                        }
                    )
                players_list.append(folder)

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
        context["page_range"] = movies.paginator.get_elided_page_range(
            movies.number, on_each_side=9, on_ends=1
        )
        return context

    def get_movies(self):
        queryset = self.object.movies.all().order_by("-created_on")
        paginator = Paginator(queryset, 24)  # paginate_by
        page = self.request.GET.get("page")
        movies = paginator.get_page(page)
        print(movies.paginator.page_range.stop)
        return movies
