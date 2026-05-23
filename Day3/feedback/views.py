from django.shortcuts import render
from django.contrib import messages
from .forms import FeedbackForm
from .models import Feedback

def feedback_form(request):
    if request.method=='POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your feedback has been submitted successfully!')
            form=FeedbackForm()
        else:
            messages.error(request,'There was an error submitting your feedback. Please try again.')
            form=FeedbackForm()
    else:
        form = FeedbackForm()
    
    return render(request,'feedback/index.html', {'form': form})