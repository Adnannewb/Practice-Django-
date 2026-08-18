from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import RecipeForm,RegistrationForm
from .models import Recipe

# Create your views here.

def home(request):
    recipes=Recipe.objects.all()
    return render(request,'home.html',{"recipes":recipes})

@login_required
def add_recipe(request):
    if request.method=='POST':
        form=RecipeForm(request.POST,request.FILES)
        if form.is_valid():
            recipe=form.save(commit=False)
            recipe.owner=request.user
            recipe.save()
            messages.success(request,'Recipe Added Successfully')
            return redirect('home')
    else:
        form=RecipeForm()
    return render(request,'recipe_form.html',{'form':form})

def update_recipe(request,pk):
    recipe=get_object_or_404(Recipe,pk=pk)
    if request.method=='POST':
        form=RecipeForm(request.POST,request.FILES,instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request,'Recipe Updated Successfully')
            return redirect('home')
    else:
        form=RecipeForm(instance=recipe)
    return render(request,'recipe_form.html',{'form':form})

def delete_recipe(request,pk):
    recipe=get_object_or_404(Recipe,pk=pk)
    if request.method=='POST':
        recipe.delete()
        return redirect('home')
    return render(request,'delete_recipe.html')

def register_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            messages.success(request,'User Registration Successful')
            login(request,user)
            return redirect('dashboard',pk=request.user.pk)
    else:
        form=RegistrationForm()
    return render(request,'register.html',{"form":form})
def login_view(request):
    next_url=request.POST.get('next') or request.GET.get('next')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            messages.success("Login Successful")
            login(request,user)
            redirect('home' or next_url)
        else:
            messages.error("Invalid Username or Password")
    return render(request,'login.html',{'next':next_url})

def logout_view(request):
    logout(request)
    return render(request,'login.html')

def dashboard(request,pk):
    pk=get_object_or_404(User,pk=pk)
    recipes=Recipe.objects.all()
    if recipes:
        recipes=recipes.filter(owner=pk)
    return render(request,'dashboard.html',{'recipes':recipes})