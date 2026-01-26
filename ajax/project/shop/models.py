from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.FloatField(default=0)
    rating_count = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.name)
