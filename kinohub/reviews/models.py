from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from django.utils.timezone import now
from movies.models import Movie


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
    LIKE_CHOICES = [(LIKE, "Подобається"), (DISLIKE, "Не подобається")]

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
        verbose_name = "Вподобайка"
        verbose_name_plural = "Вподобайки"

    def __str__(self):
        action = "подобається" if self.value == self.LIKE else "не подобається"
        return f"{self.user.username} {action} {self.content_object.pk}"
