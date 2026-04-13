from django.db import models
from django.urls import reverse
from slugify import slugify


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
