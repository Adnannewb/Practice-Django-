from django.db import models
from django.urls import reverse
# Create your models here.

class Task(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    is_completed=models.BooleanField(default=False)
    end_date=models.DateTimeField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"pk": self.pk})
    