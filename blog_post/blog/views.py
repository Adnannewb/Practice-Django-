from django.shortcuts import render
from.models import Post
from .serializers import PostSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import IsAuthorOrAdminOrReadOnly

# Create your views here.

class PostViewset(viewsets.ModelViewSet):
    queryset=Post.objects.filter(is_published=True)
    serializer_class=PostSerializer
    permission_classes=[IsAuthorOrAdminOrReadOnly]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(is_published=True) 
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)