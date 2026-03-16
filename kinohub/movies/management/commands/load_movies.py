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
        json_path = app_path / "static" / "movies" / "movies.json"

        movies = []
        with open(json_path, encoding="utf-8") as f:
            movies = json.load(f)
        if not movies:
            raise CommandError("Movies file is empty")

        return movies

    def get_or_create_movie_category(self, url):
        category = "undefined"
        if "seriesss" in url:
            category = "Серіали"
        elif "filmy" in url:
            category = "Фільми"
        elif "cartoon" in url:
            category = "Мультфільми"
        elif "animeukr" in url:
            category = "Аніме"
        elif "spilno-prodakshn":
            category = "СпільноПродакшн"
        return Category.objects.get_or_create(name=category, slug=slugify(category))[0]

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

    def proccess_movie(self, movie):
        # get movie category
        category = self.get_or_create_movie_category(movie["url"])
        uk_title = movie["uk_title"]
        en_title = movie["en_title"]
        description = movie["description"]
        image_url = movie["poster_url"]
        full_quality = movie["quality"]
        imdb_rating = movie.get("imdb_rating")
        imdb_votes = movie.get("imdb_votes")
        release_year = movie.get("year")
        genres = []
        if movie.get("genres"):
            genres = self.get_or_create_genres(movie["genres"])
        actors = []
        if movie.get("actors"):
            actors = self.get_or_create_actors(movie.get("actors"))

        self.get_or_create_movie(
            category=category,
            title=uk_title,
            en_title=en_title,
            description=description,
            image_url=image_url,
            full_quality=full_quality,
            imdb=imdb_rating,
            imdb_votes=imdb_votes,
            release_year=release_year,
            genres=genres,
            actors=actors,
        )

    def handle(self, *args, **kwargs):
        # load all movies in db
        movies = self.get_movies()
        with transaction.atomic():
            for movie in tqdm(movies, desc="Processing", unit="movie"):
                self.proccess_movie(movie)
        self.stdout.write(self.style.SUCCESS("🏁 DONE"))
