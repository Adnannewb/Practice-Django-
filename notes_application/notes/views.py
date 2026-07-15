from django.shortcuts import render,get_object_or_404,redirect
from django.db.models import Q
from .models import Note
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def home(request):
    notes=Note.objects.all()
    search=request.GET.get('search')
    if search:
        notes=notes.filter(
            Q(title__icontains=search) 
            | Q(content__icontains=search) 
            
        )
    
    return render(request,'home.html',{"notes":notes})
@login_required
def create_note(request):
    if request.method=="POST":
        title=request.POST.get('title')
        content=request.POST.get('content')
        is_favourite=request.POST.get('is_favourite')=="on"
        Note.objects.create(title=title,content=content,is_favourite=is_favourite)
        return redirect('home')
    return render(request,'create_note.html')

@login_required
def update_note(request,pk):
    note=get_object_or_404(Note,pk=pk)
    if request.method=="POST":
        note.title=request.POST.get('title')
        note.content=request.POST.get('content')
        note.is_favourite=request.POST.get('is_favourite')=="on"
        note.save()
        return redirect('home')
    return render(request,'update_note.html',{"note":note})
@login_required
def delete_note(request,pk):
    note=get_object_or_404(Note,pk=pk)
    if request.method=="POST":
        note.delete()
        return redirect('home')
    return render(request,'delete_note.html',{"note":note})

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Registration Successful")
            return redirect('dashboard')
    else:
        form=RegisterForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    next_url=request.POST.get('next') or request.GET.get('next')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login Successful")
            return redirect(next_url or 'dashboard')
        messages.error(request,"Invalid username or Password")

    return render(request,'login.html',{'next':next_url})


def logout_view(request):
    logout(request)
    return render(request,'login.html')
def dashboard(request):
    notes=Note.objects.all()
    return render(request,'dashboard.html',{'notes':notes})
            