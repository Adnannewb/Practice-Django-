from django.db import models
from django.contrib.auth.models import User
# Create your models here.
def user_photo_path(instance, filename):
    return f'photos/{instance.uploader.username}/{filename}'
class Photo(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to=user_photo_path)
    uploader=models.ForeignKey(User,on_delete=models.CASCADE)
    private=models.BooleanField(default=True)
    uploaded_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title