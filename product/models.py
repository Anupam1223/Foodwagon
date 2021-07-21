from django.db import models
from login.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    price = models.FloatField(max_length=100)
    image = models.ImageField(upload_to = 'images/')
    trader = models.ForeignKey(User, on_delete= models.CASCADE)

    def __str__(self):
        return self.name
