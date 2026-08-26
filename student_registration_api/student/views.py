from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from .serializers import StudentProfileSerializer,StudentRegistrationSerializer
from .models import StudentProfile
from django.contrib.auth.models import User
from rest_framework.response import Response
# Create your views here.

@api_view(['GET'])
@permission_classes([AllowAny])
def get_student(request):
    students=StudentProfile.objects.all()
    serializer=StudentProfileSerializer(students,many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def student_register(request):
    
    serializer=StudentRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
        "message": "Student registered successfully."
    })
    return Response(serializer.errors)

@api_view(['GET','PATCH'])
@permission_classes([IsAuthenticated])
def student_profile(request):
    student=request.user.student_profile
    if request.method=="GET":
        
        serializer=StudentProfileSerializer(student)
        return Response(serializer.data)
    elif(request.method=='PATCH'):
        
        serializer=StudentProfileSerializer(student,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
    


