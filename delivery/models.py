from django.db import models
from login.models import User
from product.models import Product
import datetime

# Create your models here.
class Order(models.Model):
    date_of_order = models.DateField(default=datetime.date.today)
    time = models.CharField(max_length=100)
    day = models.DateField(max_length=100)
    address = models.CharField(max_length=100)
    streetaddress = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    postal = models.IntegerField(max_length=100)
    country = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=5, decimal_places=1)
    token = models.CharField(max_length=500, default="asdadasdasdada")


class Order_details(models.Model):
    price = models.DecimalField(max_digits=5, decimal_places=1)
    quantity = models.IntegerField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
