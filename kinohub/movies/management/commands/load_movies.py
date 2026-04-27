import json
import re
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.utils import IntegrityError
from django_countries import countries
from slugify import slugify
from tqdm import tqdm

from movies.models import (
    Actor,
    Category,
    Director,
    Genre,
    Movie,
    Player,
    Screenshot,
    Subtitle,
)

ALIASES = {
    "сша": "US",
}


class Command(BaseCommand):
    help = "Load all movies from json to database"

    def get_movies(self):
        json_path = settings.BASE_DIR / "static" / "movies.json"

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

    def get_or_create_countries(self, country_names):

        name_to_code = {name.lower(): code for code, name in countries}
        result = []

        for name in country_names:
            key = name.lower()

            if key in ALIASES:
                result.append(ALIASES[key])
            elif key in name_to_code:
                result.append(name_to_code[key])

        return result

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

    def get_or_create_directors(self, director_names):
        directors = []
        for name in director_names:
            try:
                directors.append(
                    Director.objects.get_or_create(name=name, slug=slugify(name))[0]
                )
            except IntegrityError:
                directors.append(Director.objects.get(slug=slugify(name)))
        return directors

    def get_or_create_movie(
        self, genres, actors, directors, players, screenshots, **kwargs
    ):
        movie = Movie.objects.get_or_create(**kwargs)[0]
        movie.genres.set(genres)
        movie.actors.set(actors)
        movie.directors.set(directors)
        for url in screenshots:
            Screenshot.objects.create(movie=movie, screenshot_url=url)
        movie.save()
        for player in players:
            player_ = Player(title=player["title"], movie=movie)
            player_.save()
            if len(player["items"]) > 1:
                movie.movie_type = movie.SERIES
                movie.save()
                for episode, item in enumerate(player["items"], start=1):
                    items = player_.items.create(
                        url=item["url"],
                        poster_url=item["poster_url"],
                        episode_number=episode,
                    )
                    for lang, url in item["subtitles"].items():
                        Subtitle.objects.create(item=items, label=lang, file=url).save()
            else:
                movie.movie_type = movie.FILM
                movie.save()
                for item in player["items"]:
                    items = player_.items.create(
                        url=item["url"], poster_url=item["poster_url"]
                    )
                for lang, url in item["subtitles"].items():
                    Subtitle.objects.create(item=items, label=lang, file=url).save()

        return movie

    def normalize_age_rating(self, value):
        if not value:
            return None

        value = str(value).strip().upper()

        if value.isdigit():
            return f"{value}+"

        valid_choices = {choice[0] for choice in Movie.AGE_CHOICES}
        return value if value in valid_choices else None

    def process_streams(self, streams):
        voices = defaultdict(list)
        for stream in streams:
            if not stream.get("stream_url"):
                continue
            if stream["voice"] is not None:
                voices[stream["voice"]].append(stream)
            else:
                voices["default"].append(stream)

        players = []
        for voice in voices:
            player = {
                "title": voice,
                "items": [
                    {
                        "url": item["stream_url"],
                        "poster_url": item.get("poster_url"),
                        "subtitles": self.process_subtitles(item.get("subtitle")),
                    }
                    for item in voices[voice]
                ],
            }
            if player["items"]:
                players.append(player)

        return players

    def process_subtitles(self, subtitles):
        if not subtitles:
            return {}
        subs = {}
        matches = re.findall(r"\[(.*?)\](https?://[^\s,]+)", subtitles)
        for lang, url in matches:
            subs[lang] = url
        return subs

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
        raw_age_rating = movie.get("age_rating")
        age_rating = self.normalize_age_rating(raw_age_rating)
        trailer_url = movie.get("trailer_url")
        duration = movie.get("duration")
        countries = []
        if movie.get("country"):
            countries = self.get_or_create_countries(movie["country"])
        genres = []
        if movie.get("genres"):
            genres = self.get_or_create_genres(movie["genres"])
        actors = []
        if movie.get("actors"):
            actors = self.get_or_create_actors(movie["actors"])
        directors = []
        if movie.get("director"):
            directors = self.get_or_create_directors(movie["director"])
        players = []
        if movie.get("streams"):
            players = self.process_streams(movie["streams"])

        screenshots = movie.get("screenshots", [])

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
            age_rating=age_rating,
            trailer_url=trailer_url,
            duration=duration,
            genres=genres,
            actors=actors,
            country=countries,
            directors=directors,
            players=players,
            screenshots=screenshots,
        )

    def handle(self, *args, **kwargs):
        movies = self.get_movies()
        failed = 0
        for movie in tqdm(movies, desc="Processing", unit="movie"):
            try:
                with transaction.atomic():
                    self.proccess_movie(movie)
            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.WARNING(f"Skipped '{movie.get('uk_title')}': {e}")
                )
        self.stdout.write(self.style.SUCCESS(f"🏁 DONE — {failed} skipped"))
