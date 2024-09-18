from django.db import models
from django.core.validators import URLValidator, MinValueValidator, MaxValueValidator
from django.conf import settings

from util.shortcuts import User

# Create your models here.
class Url(models.Model):

    url = models.TextField(
        validators=[URLValidator()],
    )

    unique_identifier = models.CharField(
        max_length=settings.URL_UNIQUE_IDENTIFIERS_LENGTH,
    )

    visits = models.IntegerField(
        default=0,
    )

    allowed_visits = models.PositiveBigIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10000000000)]
    )

    expiration_datetime = models.DateTimeField(
        null=True,
        blank=True,
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.url


class Visit(models.Model):
    visit_datetime = models.DateTimeField(
        auto_now_add=True,
    )

    user_agent = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    referrer = models.CharField(
        max_length=256,
        null=True,
        blank=True,
    )

    url = models.ForeignKey(
        to=Url,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.ip_address or  self.visit_datetime