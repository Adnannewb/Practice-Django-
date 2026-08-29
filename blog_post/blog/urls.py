from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router=DefaultRouter()
router.register('post',views.PostViewset,basename='post')
router.register('comments', views.CommentViewSet, basename='comments')


urlpatterns = [
    path('',include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]