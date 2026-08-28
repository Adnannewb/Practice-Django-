from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        write_only=True,
        required=True
    )

    password = serializers.CharField(
        write_only=True,
        required=True
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True
    )

    class Meta:
        model = Employee
        fields = [
            'name',
            'email',
            'password',
            'password2',
            'department',
            'salary',
            'joining_date',
            'status',
            'role',
        ]

    def validate_email(self, value):

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                'Email already exists.'
            )

        return value

    def validate_salary(self, value):

        if value <= 0:
            raise serializers.ValidationError(
                'Salary must be greater than 0.'
            )

        return value

    def validate(self, attrs):

        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                'password2': 'Passwords do not match.'
            })

        return attrs

    def create(self, validated_data):

        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('password2')

        name = validated_data.pop('name')

        hashed_password = make_password(password)

        user = User.objects.create(
            username=email,
            email=email,
            password=hashed_password
        )

        employee = Employee.objects.create(
            user=user,
            name=name,
            **validated_data
        )

        return employee
    
    
class EmployeeProfileSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'name',
            'email',
            'department',
            'salary',
            'joining_date',
            'status',
        ]

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        request = self.context.get('request')

        if request:

            user = request.user

            if (
                user.is_authenticated
                and not user.is_staff
                and not (
                    hasattr(user, 'employee_profile')
                    and user.employee_profile.role == 'manager'
                )
            ):
                self.fields['salary'].read_only = True