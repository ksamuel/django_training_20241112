from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128)
    price = models.FloatField(
        validators=[MinValueValidator(0.0)],
    )

    def __str__(self):
        return self.name


class Sale(models.Model):
    count = models.PositiveBigIntegerField(validators=[MinValueValidator(1)])
    datetime = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="sales"
    )

    def __str__(self):
        return f"Vente de {self.count} {self.product.name}"


class SalePoint(models.Model):
    name = models.CharField(max_length=128)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.name
