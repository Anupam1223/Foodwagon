from django.db import models
from login.models import User


class Categories(models.Model):
    name = models.CharField(max_length=100, default="street food", unique=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField(max_length=100)
    image = models.ImageField(upload_to="images/food/")
    trader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ("name", "trader")


class Offer(models.Model):
    offer_amount = models.DecimalField(max_digits=5, decimal_places=1)
    trader_offer = models.ForeignKey(User, on_delete=models.CASCADE)
    product_offer = models.ForeignKey(Product, on_delete=models.CASCADE)
    offer_time = models.IntegerField()
