from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    department=models.CharField(50)
    cgpa=models.FloatField(default=0.0)
    phone=models.IntegerField()
    
    def __str__(self):
        return self.name