from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    profile_image = models.ImageField(
        null=True, blank=True, upload_to="images/", default="images/default-avatar.png"
    )
