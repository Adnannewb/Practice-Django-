from django.db.models.signals import post_save,pre_save,post_delete
from django.dispatch import receiver
from .models import Task

@receiver(pre_save,sender=Task)
def task_pre_save(sender,instance,**kwargs):
    print(f"Task Pre save: {instance.title}")
    
@receiver(post_save,sender=Task)
def task_post_save(sender,instance,created,**kwargs):
    if created:
        print(f"Task Created Successfully: {instance.title}({instance.id})")
    else:
        print(f"Task updated Successfully: {instance.title}({instance.id})")
        
@receiver(post_delete,sender=Task)
def task_delete_post_delete(sender,instance,**kwargs):
    print(f"Task deleted Successfully: {instance.title}")