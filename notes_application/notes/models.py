from django.db import models

# Create your models here.
class Note(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    is_favourite=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    