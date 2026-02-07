import json
from pathlib import Path

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from slugify import slugify
from tqdm import tqdm

from movies.models import Actor, Category, Genre, Movie


class Command(BaseCommand):
    help = "Load all movies from json to database"

    def get_movies(self):
        app_path = Path(apps.get_app_config("movies").path)
        ndjson_path = app_path / "static" / "movies" / "movies.ndjson"

        movies = []
        with open(ndjson_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    movies.append(json.loads(line))
        if not movies:
            raise CommandError("Movies file is empty")

        return movies

    def get_or_create_movie_category(self, url):
        raw_category = url.split("/")
        match raw_category[3]:  # category slug
            case "seriesss":
                category = "Серіали"
            case "filmy":
                category = "Фільми"
            case "cartoon":
                category = "Мультфільми"
            case "animeukr":
                category = "Аніме"
            case "spilno-prodakshn":
                category = "СпільноПродакшн"
            case _:
                category = raw_category[3]
        return Category.objects.get_or_create(name=category, slug=slugify(category))[0]

    def proccess_data(self, imdb, release_year):
        imdb = imdb.replace(",", ".") if imdb else "0"
        imdb = float(imdb) if imdb not in ("null", "n/A") else 0.0

        if not release_year or release_year == "null":
            release_year = 0
        elif "-" in release_year:
            release_year = int(release_year.split("-")[0])
        else:
            release_year = int(release_year)

        return imdb, release_year

    def get_or_create_genres(self, genre_names):
        genres = []
        for name in genre_names:
            genres.append(Genre.objects.get_or_create(name=name, slug=slugify(name))[0])
        return genres

    def get_or_create_actors(self, actor_names):
        actors = []
        for name in actor_names:
            try:
                actors.append(
                    Actor.objects.get_or_create(name=name, slug=slugify(name))[0]
                )
            except IntegrityError:
                actors.append(Actor.objects.get(slug=slugify(name)))
        return actors

    def get_or_create_movie(self, genres, actors, **kwargs):
        movie = Movie.objects.get_or_create(**kwargs)[0]
        movie.genres.set(genres)
        movie.actors.set(actors)
        movie.save()
        return movie

    def proccess_players(self, movie, players):
        for player_data in players.values():
            title = player_data["title"]
            player = movie.players.get_or_create(title=title)[0]
            if len(player_data["items"]) > 1:
                movie.movie_type = Movie.SERIES
                movie.save()
                for episode, url in enumerate(player_data["items"], start=1):
                    player.items.create(url=url, episode_number=episode)

            elif len(player_data["items"]) == 1:
                movie.movie_type = Movie.FILM
                movie.save()
                player.items.get_or_create(url=player_data["items"][0])

    @transaction.atomic
    def proccess_movie(self, movie):
        with transaction.atomic():
            # get movie category
            category = self.get_or_create_movie_category(movie["url"])
            title = movie["title"]
            description = movie["desc"]
            image_url = movie["image_url"]
            full_quality = movie["full_quality"]
            imdb, release_year = self.proccess_data(movie["imdb"], movie["release"])
            genres = self.get_or_create_genres(movie["genres"])
            actors = self.get_or_create_actors(movie["actors"])

            new_movie = self.get_or_create_movie(
                category=category,
                title=title,
                description=description,
                image_url=image_url,
                full_quality=full_quality,
                imdb=imdb,
                release_year=release_year,
                genres=genres,
                actors=actors,
            )
            self.proccess_players(new_movie, movie["players"])

    def handle(self, *args, **kwargs):
        # load all movies in db
        movies = self.get_movies()
        with transaction.atomic():
            for movie in tqdm(movies, desc="Processing", unit="movie"):
                self.proccess_movie(movie)
        self.stdout.write(self.style.SUCCESS("🏁 DONE"))
