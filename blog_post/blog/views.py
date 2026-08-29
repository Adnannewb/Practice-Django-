from django.shortcuts import render
from.models import Post,Comment
from .serializers import PostSerializer,CommentSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import IsAuthorOrAdminOrReadOnly,IsCommentAuthorOrAdminOrReadOnly

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
        

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        
        serializer.save(commentator=self.request.user)