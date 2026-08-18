from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_photo_path(instance,filename):
    return f"photos/{instance.owner.username}/{filename}"

class Recipe(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    recipe_image=models.ImageField(upload_to=user_photo_path)
    ingredients=models.CharField()
    instructions=models.CharField()
    cooking_time=models.SmallIntegerField()
    category=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title