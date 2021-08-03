from django.db import models
from login.models import User
from product.models import Product


# Create your models here.
class Order(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    price = models.FloatField(max_length=100)
    image = models.ImageField(upload_to="images/food/")
    trader = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
