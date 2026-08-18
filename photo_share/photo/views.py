from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,PhotoForm
from .models import Photo
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    photos=Photo.objects.filter(private=False).order_by('uploaded_at')
    return render(request,'home.html',{"photos":photos})

def register_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,"Registration Successful")
            redirect('dashboard',pk=request.user.pk)
    else:
        form=RegistrationForm()
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
            return redirect(next_url or 'dashboard',pk=request.user.pk)
        else:
            messages.error("Invalid Username or Password")
    return render(request,'login.html',{'next':next_url})
def logout_view(request):
    logout(request)
    return render(request,'login.html')

def dashboard(request,pk):
    pk=get_object_or_404(User,pk=pk)
    photos=Photo.objects.all()
    if photos:
        photos=photos.filter(uploader=pk)
    return render(request,'dashboard.html',{'photos':photos})
@login_required
def image_upload(request):
    if request.method=='POST':
        form=PhotoForm(request.POST,request.FILES)
        if form.is_valid():
            photo=form.save(commit=False)
            photo.uploader=request.user
            photo.save()
            messages.success(request,'Image Uploaded Successfully')
            return redirect('dashboard',pk=request.user.pk)
    else:
        form=PhotoForm()
    return render(request,'image.html',{'form':form})

def image_update(request,pk):
    photo=get_object_or_404(Photo,pk=pk)

    if request.method=='POST':
        form=PhotoForm(request.POST,request.FILES,instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request,'Image Updated Successfully')
            return redirect('dashboard',pk=request.user.pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request,'image.html',{'form':form})

def image_delete(request,pk):
    photo=get_object_or_404(Photo,pk=pk)
    if request.method=='POST':
        photo.delete()
        messages.success(request,'Image Deleted Successfully')
        return redirect('dashboard',pk=request.user.pk)
    return render(request,'image_delete.html')
            