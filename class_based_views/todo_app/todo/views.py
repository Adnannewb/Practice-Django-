from django.shortcuts import render
from django.views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy,reverse
from .models import Task
from .forms import TaskForm
from django.http import HttpResponse
# Create your views here.


class TaskListView(ListView):
    model=Task
    template_name="home.html"
    context_object_name="tasks"
class TaskDetailView(DetailView):
    model=Task
    template_name="taskdetail.html"
    context_object_name="task"
class TaskCreateView(CreateView):
    model=Task
    template_name="taskform.html"
    form_class=TaskForm
    success_url = reverse_lazy('home')

class TaskUpdateView(UpdateView):
    model=Task
    template_name="taskform.html"
    emplate_name="taskform.html"
    form_class=TaskForm
    def get_success_url(self):
        return reverse('taskdetail', kwargs={'pk': self.object.pk})
   

class TaskDeleteView(DeleteView):
    model=Task
    template_name="taskdelete.html"
    success_url=reverse_lazy('home')
    

# session Storage part 
def set_session(request):
    request.session['username']='abul'
    request.session['course']='django'
    return HttpResponse("Session Saved Successfully")

def get_session(request):
    username=request.session.get('username','Guest')
    course=request.session.get('course','Not enrolled')
    return HttpResponse(f'Welcome, {username}. Your course: {course}')

def delete_session(request):
    request.session.flush()
    return HttpResponse("Session Deleted Successfully.")

# cookie part 
def set_cookie(request):
    response=HttpResponse("Cookie Set Successfully")
    response.set_cookie('username','Abul',max_age=60*60*24*1)
    response.set_cookie('course','Django',max_age=60*60*24*1)
    return response

def get_cookie(request):
    username=request.COOKIES.get('username','Guest')
    course=request.COOKIES.get('course','Not enrolled')
    return HttpResponse(f'Welcome, {username}. Your course: {course}')

def delete_cookie(request):
    response=HttpResponse("Cookies Deleted Successfully")
    response.delete_cookie('username')
    response.delete_cookie('course')
    return response