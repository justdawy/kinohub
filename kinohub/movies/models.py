from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from slugify import slugify


class Category(models.Model):
    icon = models.CharField(max_length=24, default="fa-film")
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    is_visible_on_home = models.BooleanField(
        default=True,
        help_text="Select whether you want to display this category on the home page",
    )
    position = models.PositiveIntegerField(
        default=0, help_text="Order of category on the main page (lower comes first)"
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter a movie genre (e.g. Drama, Horror, Comedy)",
    )
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "genre_detail",
            kwargs={"genre_slug": self.slug},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Actor(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter an actor's name (e.g. Tobey Maguire)",
    )
    slug = models.SlugField(unique=True, blank=True, max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "actor_detail",
            kwargs={"actor_slug": self.slug},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):
    FILM = 1
    SERIES = 2

    MOVIE_TYPE_CHOICES = [
        (FILM, "Film (few dubs)"),
        (SERIES, "Series (episodes)"),
    ]
    movie_type = models.PositiveSmallIntegerField(choices=MOVIE_TYPE_CHOICES, default=1)

    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="movies"
    )
    title = models.CharField(max_length=255)
    slug = models.SlugField(blank=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    full_quality = models.CharField(max_length=50, blank=True, null=True)
    imdb = models.FloatField(blank=True, null=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, help_text="Select a genre for this book")
    actors = models.ManyToManyField(Actor, help_text="Select an actor for this movie")
    created_on = models.DateTimeField("Date published", default=now)
    changed_on = models.DateTimeField("Date edited", auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "movie_detail",
            kwargs={"category_slug": self.category.slug, "movie_slug": self.slug},
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Player(models.Model):
    movie = models.ForeignKey(Movie, related_name="players", on_delete=models.CASCADE)
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title + "\n" + self.movie.title


class Item(models.Model):
    player = models.ForeignKey(Player, related_name="items", on_delete=models.CASCADE)
    url = models.URLField()
    episode_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.episode_number:
            return (
                f"{self.player.title}\n"
                f"{self.player.movie.title}\n"
                f"Episode {self.episode_number}"
            )
        return f"{self.player.title}\n{self.player.movie.title}"


class Subtitle(models.Model):
    item = models.ForeignKey(Item, related_name="subtitles", on_delete=models.CASCADE)
    label = models.CharField(max_length=30)
    file = models.URLField()

    def __str__(self):
        return f"{self.label} - {self.item}"
