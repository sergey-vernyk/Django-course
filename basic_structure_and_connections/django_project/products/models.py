from decimal import Decimal

from django.db import models
from django.urls import reverse


class Product(models.Model):
    """Модель товару."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=255)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    rating = models.DecimalField(default=Decimal(0.0), max_digits=2, decimal_places=1)

    def get_absolute_url(self) -> str:
        """
        Функція повертає абсолютну адресу URL для об'єкта товару.
        Приклад http://127.0.0.1:8000/products/3/samsung/
        """
        return reverse(
            # 'product_detail' назву беремо з локального файлу 'urls.py'
            # з параметру 'name'
            "product_detail",
            kwargs={"product_pk": self.pk, "product_slug": self.slug},
        )
