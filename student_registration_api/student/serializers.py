from rest_framework import serializers
from .models import StudentProfile
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class StudentRegistrationSerializer(serializers.ModelSerializer):
    
    name=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    age=serializers.IntegerField(required=True)
    phone=serializers.CharField(required=False)
    password=serializers.CharField(write_only=True,required=True)
    password2=serializers.CharField(write_only=True,required=True)
    
    class Meta:
        model=User
        fields = ['name', 'username', 'email', 'age', 'phone', 'password', 'password2']
    
    def validate_email(self,value):
        if (User.objects.filter(email=value).exists()):
            raise serializers.ValidationError("Email Already Exists.")
        return value
    def validate_username(self,value):
        if (User.objects.filter(username=value).exists()):
            raise serializers.ValidationError("Username Already Exists.")
        return value
    def validate_age(self, value):
        if value < 18:
            raise serializers.ValidationError("You must be 18 or older.")
        return value
    def validate(self,data):
        if(data.get('password')!=data.get('password2')):
            raise serializers.ValidationError('Password does not match!')
        return data
        
    def create(self, validated_data):
        age=validated_data.pop('age')
        phone=validated_data.pop('phone','')
        name=validated_data.pop('name')
        plain_password=validated_data.pop('password')
        validated_data.pop('password2')
        hashed_password= make_password(plain_password)
        
        user=User.objects.create(
            password=hashed_password,
            **validated_data,
        )
        StudentProfile.objects.create(
            user=user,
            name=name,
            age=age,
            phone=phone,
        )
        
        return user
    

class StudentProfileSerializer(serializers.ModelSerializer):
    
    email=serializers.EmailField(source='user.email',read_only=True)
    class Meta:
        model=StudentProfile
        fields=['name','age','phone','email']
    
    def update(self, instance, validated_data):
        instance.name=validated_data.get('name',instance.name)
        instance.age=validated_data.get('age',instance.age)
        instance.phone=validated_data.get('phone',instance.phone)
        instance.save()
        return instance
        
