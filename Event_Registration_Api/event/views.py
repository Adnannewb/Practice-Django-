from django.shortcuts import render
from rest_framework import viewsets
from .models import Registration,Event
from .serializers import RegistrationSerializer
from django.contrib.auth.models import User
from .permissions import CustomPermissions
# Create your views here.

class RegistrationViewset(viewsets.ModelViewSet):
    queryset=Registration.objects.all()
    serializer_class=RegistrationSerializer
    permission_classes=[CustomPermissions]
    
        
