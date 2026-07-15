from django.db import models

# Create your models here.

class Transaction(models.Model):
    types=[
        "Income",
        "Expense"
    ]
    title=models.CharField(max_length=100)
    amount=models.BigIntegerField()
    type=models.CharField(max_length=10, choices=[(t, t) for t in types])
    date=models.DateTimeField(auto_now_add=True)
    category=models.CharField(max_length=100)
    
    def __str__(self):
        return self.title