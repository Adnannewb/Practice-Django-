from django.db import models

# Create your models here.
class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    publisher=models.CharField(max_length=100)
    price=models.FloatField(default=0)
    quantity=models.IntegerField(default=0)
    
    def __str__(self):
        return self.title