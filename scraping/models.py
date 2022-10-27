from django.db import models


class City(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.CharField(max_length=32, blank=True, unique=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f'{self.name}'
