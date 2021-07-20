from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=10)
    stock = models.IntegerField()
    price = models.FloatField(max_length=100)

    def __str__(self):
        return self.name
