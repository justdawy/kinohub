from django.db import models


class Player(models.Model):
    movie = models.ForeignKey(
        "Movie", related_name="players", on_delete=models.CASCADE, verbose_name="Фільм"
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
