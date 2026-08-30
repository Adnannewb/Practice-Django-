from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    capacity=models.PositiveIntegerField()
    date=models.DateTimeField()
    
    def __str__(self):
        return self.title

class Registration(models.Model):
    event=models.ForeignKey(Event,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    registered_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['event', 'user'],
                name='unique_event_user_registration'
            )
        ]
    def __str__(self):
        return self.user.username


