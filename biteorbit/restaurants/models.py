from django.db import models

class Restaurant(models.Model):

    name = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='restaurants/',
        blank=True,
        null=True
    )

    description = models.TextField()

    rating = models.CharField(max_length=10)

    delivery_time = models.CharField(max_length=100)

    def __str__(self):
        return self.name