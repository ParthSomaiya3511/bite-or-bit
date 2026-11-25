from django.db import models
from restaurants.models import Restaurant

class Food(models.Model):

    restaurant = models.ForeignKey(

        Restaurant,

        on_delete=models.CASCADE,

        related_name="foods",

        null=True,
        blank=True
    )


    name = models.CharField(max_length=200)

    image = models.ImageField(
        upload_to='foods/',
        blank=True,
        null=True
    )

    description = models.TextField()

    price = models.IntegerField()

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name