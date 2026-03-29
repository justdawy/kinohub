from django.conf import settings
from django.core.paginator import Paginator
from django.views import generic

from movies.forms import SearchForm
from movies.models import Actor, Category, Movie


class SearchListView(generic.ListView):
    model = Movie
    template_name = "movies/search.html"
    context_object_name = "movies"
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.request.GET.get("title")
        return context

    def get_queryset(self):
        # filter by title
        title: str = self.request.GET.get("title")
        if not title:
            return []
        elif title.isascii():
            return Movie.objects.filter(en_title__icontains=title).order_by(
                "-changed_on"
            )
        else:
            return Movie.objects.filter(title__icontains=title).order_by("-changed_on")


class MovieDetailView(generic.DetailView):
    model = Movie
    template_name = "movies/movie_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "movie_slug"

    def get_queryset(self):
        #  filter by category
        return Movie.objects.filter(
            category__slug=self.kwargs.get("category_slug"),
            slug=self.kwargs.get("movie_slug"),
            id=self.kwargs.get("id"),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        players_list = []
        if self.object.movie_type == Movie.FILM:
            for player in self.object.players.all():
                for player_item in player.items.all():
                    subtitles_str = ""
                    for subtitle in player_item.subtitles.all():
                        subtitles_str += f"[{subtitle.label}]{subtitle.file},"

                    if player_item.player.title == "default":
                        title = "Звичайний"
                    else:
                        title = player_item.player.title
                    players_list.append(
                        {
                            "title": title,
                            "file": settings.PROXY_URL + player_item.url,
                            "poster": player_item.poster_url,
                            "subtitle": subtitles_str,
                        }
                    )
        elif self.object.movie_type == Movie.SERIES:
            for player in self.object.players.all():
                folder = {"title": player.title, "folder": []}
                for player_item in player.items.all():
                    subtitles_str = ""
                    for subtitle in player_item.subtitles.all():
                        subtitles_str += f"[{subtitle.label}]{subtitle.file},"

                    folder["folder"].append(
                        {
                            "title": f"Серія {player_item.episode_number}",
                            "file": settings.PROXY_URL + player_item.url,
                            "poster": player_item.poster_url,
                            "subtitle": subtitles_str,
                        }
                    )
                players_list.append(folder)

        context["players_list"] = players_list
        movie_reviews = self.object.reviews.filter(parent__isnull=True).order_by(
            "-created_on"
        )
        context["movie_reviews"] = movie_reviews
        return context


class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = "movies/category_view.html"
    slug_field = "slug"
    slug_url_kwarg = "category_slug"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        genres = self.object.genres_in_filter.all()
        form = SearchForm(self.request.GET, genres=genres)

        # copy GET params except "page"
        querydict = self.request.GET.copy()
        querydict.pop("page", None)

        context["query_string"] = querydict.urlencode()

        if not form.is_valid():
            movies = self.get_movies()
            context["movies"] = movies
            context["page_range"] = movies.paginator.get_elided_page_range(
                movies.number, on_each_side=9, on_ends=1
            )
        else:
            filters = {}

            title = form.cleaned_data.get("title")
            if title.isascii():
                filters["en_title__icontains"] = title
            else:
                filters["title__icontains"] = title

            genre = form.cleaned_data.get("genres")
            if genre:
                filters["genres__name"] = genre

            min_rating = form.cleaned_data.get("min_imdb_rating")
            if min_rating is not None:
                filters["imdb__gte"] = min_rating

            year = form.cleaned_data.get("year")
            if year:
                filters["release_year"] = year

            movies = self.get_movies(search=True, **filters)
            context["movies"] = movies
            context["page_range"] = movies.paginator.get_elided_page_range(
                movies.number, on_each_side=9, on_ends=1
            )
        context["form"] = form
        return context

    def get_movies(self, search=False, **kwargs):
        if not search:
            queryset = self.object.movies.all().order_by("-changed_on")
        else:
            queryset = self.object.movies.filter(**kwargs).order_by("-changed_on")
        paginator = Paginator(queryset, 24)  # paginate_by
        page = self.request.GET.get("page")
        movies = paginator.get_page(page)
        return movies


class ActorDetailView(generic.DetailView):
    model = Actor
    template_name = "movies/actor_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "actor_slug"
    context_object_name = "actor"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movies = self.get_movies()
        context["movies"] = movies
        context["page_range"] = movies.paginator.get_elided_page_range(
            movies.number, on_each_side=9, on_ends=1
        )
        return context

    def get_movies(self, **kwargs):
        queryset = Movie.objects.filter(actors__name=self.object.name).order_by(
            "-changed_on"
        )
        paginator = Paginator(queryset, 24)
        page = self.request.GET.get("page")
        movies = paginator.get_page(page)
        return movies


class AbuseTemplateView(generic.TemplateView):
    template_name = "movies/right_holders.html"
