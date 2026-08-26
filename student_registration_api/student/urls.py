from django.urls import path,include
from .import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
     # Route to submit username/password and receive access + refresh tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Route to submit a refresh token and get a brand-new access token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/",views.student_register),
    path("profile/",views.student_profile),
    path("students/",views.get_student),
]