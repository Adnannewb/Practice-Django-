from django.shortcuts import get_object_or_404

from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes
)

from .models import Employee
from .serializers import (
    EmployeeSerializer,
    EmployeeProfileSerializer
)
from .permissions import IsManager

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_employee(request):

    serializer = EmployeeSerializer(
        data=request.data
    )

    if serializer.is_valid():
        serializer.save()

        return Response({
            'message': 'Employee created successfully.'
        })

    return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsManager])
def manage_employee(request):

    employees = Employee.objects.all()

    serializer = EmployeeProfileSerializer(
        employees,
        many=True,
        context={'request': request}
    )

    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def employee_profile(request):

    employee = get_object_or_404(
        Employee,
        user=request.user
    )

    serializer = EmployeeProfileSerializer(
        employee,
        context={'request': request}
    )

    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_employee_profile(request):

    employee = get_object_or_404(
        Employee,
        user=request.user
    )

    serializer = EmployeeProfileSerializer(
        employee,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)

@api_view(['PATCH'])
@permission_classes([IsManager])
def update_employee(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    serializer = EmployeeProfileSerializer(
        employee,
        data=request.data,
        partial=True,
        context={'request': request}
    )

    if serializer.is_valid():
        serializer.save()

        return Response(serializer.data)

    return Response(serializer.errors)