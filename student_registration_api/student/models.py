from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="student_profile")
    name=models.CharField(max_length=50)
    age=models.PositiveIntegerField()
    phone=models.CharField(max_length=12,blank=True,null=True)
    
    def __str__(self):
        return self.user.username
    