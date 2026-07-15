from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.db.models import Q
from .models import Book
from .forms import BookForm,RegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    books=Book.objects.all()
    search=request.GET.get('search','').strip()
    if search:
        books=books.filter(Q(title__icontains=search)
                           | Q(author__icontains=search)
                           |Q(publisher__icontains=search))
    
    books = books.filter(quantity__gte=1)
    return render(request,'home.html',{'books':books})
@login_required
def book_details(request,pk):
    book=get_object_or_404(Book,pk=pk)
    return render(request,'book_details.html',{'book':book})

def add_book(request):
    form=BookForm()
    if request.method=='POST':
        form=BookForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Added Successfully')
            return redirect('home')
        else:
            form=BookForm()
    return render(request,'add_book.html',{'form':form})

def update_book(request,pk):
    book=get_object_or_404(Book,pk=pk)
    if request.method=='POST':
        form=BookForm(request.POST,instance=book)
        if form.is_valid():
            form.save()
            messages.success(request,'Book Updated Successfully')
            return redirect('home')
    else:
        form=BookForm(instance=book)
    return render(request,'add_book.html',{'form':form})

def delete_book(request,pk):
    book=get_object_or_404(Book,pk=pk)
    if request.method=='POST':
        book.delete()
        messages.success(request,'Book Deleted Successfully')
        return redirect('home')
    return render(request,'delete_book.html',{'book':book})
    
    


def register_view(request):
    if request.method=='POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            messages.success(request,'Registered Successfully')
            return redirect('dashboard')
    else:
        form=RegistrationForm()
    return render(request,'register.html',{'form':form})

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'Logged in Successfully')
            return redirect(next_url or 'dashboard')
        messages.error(request,'Invalid Username or Password')
    return render(request,'login.html',{'next': next_url})

def logout_view(request):
    logout(request)
    messages.success(request,'Logged out Successfully')
    return redirect('login')

@login_required
def dashboard(request):
    books=Book.objects.all()
    return render(request,'dashboard.html',{'books':books})