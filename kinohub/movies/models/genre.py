from django.db import models
from django.urls import reverse
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
