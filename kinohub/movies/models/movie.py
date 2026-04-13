from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils.timezone import now
from django_countries.fields import CountryField
from slugify import slugify


class Movie(models.Model):
    FILM = 1
    SERIES = 2

    MOVIE_TYPE_CHOICES = [
        (FILM, "Фільм (кілька дубляжів)"),
        (SERIES, "Серіал (серії)"),
    ]
    movie_type = models.PositiveSmallIntegerField(
        choices=MOVIE_TYPE_CHOICES, default=1, verbose_name="Тип"
    )

    AGE_CHOICES = [
        ("0+", "0+"),
        ("6+", "6+"),
        ("12+", "12+"),
        ("16+", "16+"),
        ("18+", "18+"),
        # American (MPAA - movies)
        ("G", "G (General Audiences)"),
        ("PG", "PG (Parental Guidance Suggested)"),
        ("PG-13", "PG-13 (Parents Strongly Cautioned)"),
        ("R", "R (Restricted)"),
        ("NC-17", "NC-17 (Adults Only)"),
        # American (TV ratings)
        ("TV-Y", "TV-Y (All Children)"),
        ("TV-Y7", "TV-Y7 (Older Children)"),
        ("TV-G", "TV-G (General Audience)"),
        ("TV-PG", "TV-PG (Parental Guidance)"),
        ("TV-14", "TV-14 (Parents Strongly Cautioned)"),
        ("TV-MA", "TV-MA (Mature Audience)"),
    ]

    category = models.ForeignKey(
        "Category",
        on_delete=models.RESTRICT,
        related_name="movies",
        verbose_name="Категорія",
    )
    title = models.CharField(max_length=255, verbose_name="Українська назва")
    slug = models.SlugField(blank=True, max_length=255, verbose_name="URL-ім'я")
    en_title = models.CharField(max_length=255, verbose_name="Англійська назва")
    duration = models.CharField(
        max_length=20, blank=True, null=True, verbose_name="Тривалість фільму"
    )
    country = CountryField(multiple=True)
    age_rating = models.CharField(
        max_length=10, blank=True, null=True, choices=AGE_CHOICES
    )
    description = models.TextField(blank=True, null=True, verbose_name="Опис")
    image_url = models.URLField(blank=True, null=True, verbose_name="URL зображення")
    trailer_url = models.URLField(
        blank=True, null=True, verbose_name="URL-адреса трейлера"
    )
    directors = models.ManyToManyField(
        "Director",
        help_text="Виберіть режисера для цього фільму",
        verbose_name="Режисери",
    )
    full_quality = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Якість"
    )
    imdb = models.FloatField(blank=True, null=True, verbose_name="IMDb")
    imdb_votes = models.IntegerField(
        blank=True, null=True, verbose_name="Кількість голосів IMDB"
    )
    release_year = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Рік випуску"
    )
    genres = models.ManyToManyField(
        "Genre", help_text="Виберіть жанр для цього фільму", verbose_name="Жанри"
    )
    actors = models.ManyToManyField(
        "Actor", help_text="Виберіть актора для цього фільму", verbose_name="Актори"
    )
    created_on = models.DateTimeField("Дата публікації", default=now)
    changed_on = models.DateTimeField("Дата редагування", auto_now=True)

    class Meta:
        verbose_name = "Фільм"
        verbose_name_plural = "Фільми"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            "movie_detail",
            kwargs={
                "category_slug": self.category.slug,
                "movie_slug": self.slug,
                "id": self.pk,
            },
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Screenshot(models.Model):
    movie = models.ForeignKey(
        "Movie", related_name="screenshots", on_delete=models.CASCADE
    )
    screenshot_url = models.URLField(verbose_name="URL Ha Кадр із фільму")

    def __str__(self):
        return f"Кадр із фільму {self.movie.title}"


class Review(models.Model):
    movie = models.ForeignKey("Movie", related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
        blank=True,
        null=True,
    )

    guest_name = models.CharField(max_length=100, blank=True)

    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="replies", on_delete=models.CASCADE
    )
    content = models.TextField()

    created_on = models.DateTimeField("Дата публікації", default=now)
    changed_on = models.DateTimeField("Дата редагування", auto_now=True)

    class Meta:
        verbose_name = "Відгук"
        verbose_name_plural = "Відгуки"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"],
                condition=Q(parent__isnull=True),
                name="unique_user_movie_review",
            )
        ]

    def __str__(self):
        if self.user:
            return f"Відгук від {self.user.username} до {self.movie.title}"
        return f"Відгук від {self.guest_name or 'Guest'} до {self.movie.title}"

    @property
    def likes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type, object_id=self.pk, value=Like.LIKE
        ).count()

    @property
    def dislikes_count(self):
        content_type = ContentType.objects.get_for_model(self)
        return Like.objects.filter(
            content_type=content_type, object_id=self.pk, value=Like.DISLIKE
        ).count()


class Like(models.Model):
    LIKE = 1
    DISLIKE = -1
    LIKE_CHOICES = [(LIKE, "Like"), (DISLIKE, "Dislike")]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_likes"
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, related_name="content_type"
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    value = models.SmallIntegerField(choices=LIKE_CHOICES)

    class Meta:
        unique_together = ["user", "content_type", "object_id"]

    def __str__(self):
        action = "liked" if self.value == self.LIKE else "disliked"
        return f"{self.user.username} {action} {self.content_object.pk}"
