from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views


urlpatterns = [

    # Employee management
    path(
        'employees/',
        views.manage_employee
    ),

    path(
        'employees/<int:pk>/',
        views.update_employee
    ),

    # Employee own profile
    path(
        'profile/',
        views.employee_profile
    ),

    path(
        'profile/update/',
        views.update_employee_profile
    ),

    # Authentication
    path(
        'api/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]