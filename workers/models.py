from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from tasks.models import Position


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="workers",
    )

    class Meta:
        ordering = ["username"]
        verbose_name = "workers"
        verbose_name_plural = "workers"

    def get_absolute_url(self):
        return reverse("workers:workers-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.username
