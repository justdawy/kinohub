from django.db import models
from django.utils.timezone import now

class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter a movie genre (e.g. Drama, Horror, Comedy)"
    )

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Enter an actor's name (e.g. Tobey Maguire)"
    )

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    full_quality = models.CharField(max_length=50, blank=True, null=True)
    imdb = models.FloatField(blank=True, null=True)
    release_year = models.PositiveIntegerField(blank=True, null=True)
    genres = models.ManyToManyField(
            Genre, help_text="Select a genre for this book"
    )
    actors = models.ManyToManyField(
            Actor, help_text="Select an actor for this movie"
    )
    created_on = models.DateTimeField("Date published", default=now)
    changed_on = models.DateTimeField("Date edited", auto_now=True)

    def __str__(self):
        return self.title

class Player(models.Model):
    movie = models.ForeignKey(Movie, related_name='players', on_delete=models.CASCADE)
    title = models.CharField(max_length=80)

    def __str__(self):
        return self.title + "\n" + self.movie.title

class Item(models.Model):
    player = models.ForeignKey(Player, related_name='items', on_delete=models.CASCADE)
    url = models.URLField()
    episode_number = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        if self.episode_number:
            return self.player.title + '\n' + self.player.movie.title + f"\nEpisode {self.episode_number}"
        return f"{self.player.title}"
