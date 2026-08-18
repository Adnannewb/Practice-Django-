from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    def __str__(self):
        return self.name

def user_photo_path(instance, filename):
    return f'photos/{instance.user.username}/{filename}'

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.IntegerField(null=True,blank=True)
    address=models.TextField(null=True,blank=True)
    dob=models.DateField(null=True,blank=True)
    profile_picture=models.ImageField(upload_to=user_photo_path,null=True,blank=True)
    
    def __str__(self):
        return self.user.username

class Event(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    date=models.DateTimeField()
    venue=models.CharField(max_length=150)
    capacity=models.IntegerField()
    organizer=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Registration(models.Model):
    class Status(models.TextChoices):
        REGISTERED = "registered", "Registered"
        CANCELLED = "cancelled", "Cancelled"
        
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    registered_at=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=20,
                            choices=Status.choices,
                            default=Status.REGISTERED)
    class Meta:
        constraints=[
            models.UniqueConstraint(
                fields=['user','event'],
                name='unique_user_registration'
            )
        ]
    
    