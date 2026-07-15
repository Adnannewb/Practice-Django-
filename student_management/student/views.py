from django.shortcuts import render,redirect,get_object_or_404
from .models import Student
from django.urls import reverse

# Create your views here.

def student_list(request):
    students=Student.objects.all()
    
    return render(request,"student_list.html",{"students":students})

def create_student(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        department=request.POST.get("department")
        cgpa=request.POST.get("cgpa")
        phone=request.POST.get("phone")
        Student.objects.create(name=name,email=email,department=department,cgpa=cgpa,phone=phone)
        return redirect(reverse('student_list'))  
    
    return render(request,"create_student.html")

def update_student(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        student.name=request.POST.get("name")
        student.email=request.POST.get("email")
        student.department=request.POST.get("department")
        student.cgpa=request.POST.get("cgpa")
        student.phone=request.POST.get("phone")
        student.save()
        return redirect(reverse('student_list'))

    return render(request,"update_student.html",{"student":student})

def delete_student(request,pk):
    student=get_object_or_404(Student,pk=pk)
    if request.method=="POST":
        student.delete()
        return redirect(reverse("student_list"))
    return render(request,"delete_student.html",{"student":student})

def search_student(request):
    query=request.GET.get("name","").strip()
    students=Student.objects.all()

    if query:
        students=students.filter(name__icontains=query)

    return render(request,"student_list.html",{"students":students,"query":query})