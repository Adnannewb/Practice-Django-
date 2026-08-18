from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Define the fields you want to show
        fields = ['title', 'description', 'is_completed', 'end_date']
        
        # This turns the plain text box into a visual calendar picker
        widgets = {
            'end_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            ),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
        # Pop/remove the field completely from the form
            self.fields.pop('is_completed', None)
        
