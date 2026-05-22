from django.shortcuts import render

# Create your views here.

def index(request):
    students = [
        {
            "name": "Adnan Hasan",
            "marks": 85,
            "description": "Adnan is a brilliant student and performs very well in programming and database courses."
        },

        {
            "name": "Rahim Islam",
            "marks": 45,
            "description": "Rahim needs improvement in mathematics and problem solving."
        },

        {
            "name": "Karim Ahmed",
            "marks": 72,
            "description": "Karim is good at web development and Django framework."
        },

        {
            "name": "Sadia Noor",
            "marks": 63,
            "description": "Sadia is improving every semester and works hard regularly."
        },

        {
            "name": "Nusrat Jahan",
            "marks": 91,
            "description": "Nusrat is one of the top students in the department."
        }
    ]

    context = {
        'students': students
    }
    
    return render(request,'index.html',context=context)