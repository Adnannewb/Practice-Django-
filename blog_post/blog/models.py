from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Post(models.Model):
    title=models.CharField(max_length=50)
    content=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    is_published=models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    comment=models.CharField(max_length=250)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    commentator=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.comment