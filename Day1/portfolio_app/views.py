from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'portfolio_app/home.html')

def about(request):
    return render(request, 'portfolio_app/about.html')

def contact(request):
    return render(request, 'portfolio_app/contact.html')