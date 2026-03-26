from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django_countries.fields import CountryField
from slugify import slugify


class Genre(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Жанр",
        help_text="Введіть жанр фільму (наприклад: Драма, Жахи, Комедія)",
    )
    slug = models.SlugField(
        unique=True, blank=True, max_length=255, verbose_name="URL-ім'я"
    )

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанри"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("genre_detail", kwargs={"genre_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Category(models.Model):
    icon = models.CharField(max_length=24, default="fa-film", verbose_name="Іконка")
    name = models.CharField(max_length=100, unique=True, verbose_name="Назва категорії")
    singular_name = models.CharField(max_length=100, verbose_name="Назва в однині")
    slug = models.SlugField(
        unique=True, blank=True, max_length=255, verbose_name="URL-ім'я"
    )

    is_visible_on_home = models.BooleanField(
        default=True,
        verbose_name="Відображати на головній",
        help_text="Виберіть, чи відображати цю категорію на головній сторінці",
    )
    position = models.PositiveIntegerField(
        default=0,
        verbose_name="Позиція",
        help_text=(
            "Порядок відображення категорії на головній сторінці "
            "(менше значення — вище)"
        ),
    )

    genres_in_filter = models.ManyToManyField(
        Genre,
        verbose_name="Жанри у фільтрі",
        help_text="Виберіть жанри, які повинні бути "
        "видимими у фільтрі для цієї категорії",
    )

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"category_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Actor(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Актор",
        help_text="Введіть ім'я актора (наприклад: Тобі Магуайр)",
    )
    slug = models.SlugField(
        unique=True, blank=True, max_length=255, verbose_name="URL-ім'я"
    )

    class Meta:
        verbose_name = "Актор"
        verbose_name_plural = "Актори"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"actor_slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Director(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Режисер",
        help_text="Введіть ім'я режисера фільму",
    )
    slug = models.SlugField(
        unique=True, blank=True, max_length=255, verbose_name="URL-ім'я"
    )

    class Meta:
        verbose_name = "Режисер"
        verbose_name_plural = "Режисери"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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
        Category,
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
        Director,
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
        Genre, help_text="Виберіть жанр для цього фільму", verbose_name="Жанри"
    )
    actors = models.ManyToManyField(
        Actor, help_text="Виберіть актора для цього фільму", verbose_name="Актори"
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


class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name="reviews", on_delete=models.CASCADE)
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

    def __str__(self):
        if self.user:
            return f"Відгук від {self.user.username} до {self.movie.title}"
        return f"Відгук від {self.guest_name or 'Guest'} до {self.movie.title}"


class Player(models.Model):
    movie = models.ForeignKey(
        Movie, related_name="players", on_delete=models.CASCADE, verbose_name="Фільм"
    )
    title = models.CharField(max_length=256, verbose_name="Назва дубляжу")

    class Meta:
        verbose_name = "Дубляж"
        verbose_name_plural = "Дубляжі"

    def __str__(self):
        return f"{self.title} - {self.movie.title}"


class Item(models.Model):
    player = models.ForeignKey(
        Player, related_name="items", on_delete=models.CASCADE, verbose_name="Плеєр"
    )
    url = models.URLField(max_length=300, verbose_name="URL")
    poster_url = models.URLField(
        null=True, blank=True, max_length=300, verbose_name="URL-скріншот з фільму"
    )
    episode_number = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Номер серії"
    )

    class Meta:
        verbose_name = "Епізод"
        verbose_name_plural = "Епізоди"

    def __str__(self):
        if self.episode_number:
            return (
                f"{self.player.title} - {self.player.movie.title} "
                f"Серія {self.episode_number}"
            )
        return f"{self.player.title} - {self.player.movie.title}"


class Subtitle(models.Model):
    item = models.ForeignKey(
        Item, related_name="subtitles", on_delete=models.CASCADE, verbose_name="Епізод"
    )
    label = models.CharField(max_length=30, verbose_name="Мова / Назва субтитрів")
    file = models.URLField(verbose_name="Файл субтитрів")

    class Meta:
        verbose_name = "Субтитри для епізоду"
        verbose_name_plural = "Субтитри для епізодів"

    def __str__(self):
        if self.item.episode_number:
            return (
                f"{self.label} - {self.item.player.title}"
                f"({self.item.player.movie.title} Серія {self.item.episode_number})"
            )
        return (
            f"{self.label} - {self.item.player.title} ({self.item.player.movie.title})"
        )
