from django.shortcuts import render
from .serializers import ReviewSerializer
from rest_framework import viewsets
from .models import Review
from .permissions import IsReviewerOrReadOnly
# Create your views here.

class ReviewViewset(viewsets.ModelViewSet):
    queryset=Review.objects.all()
    serializer_class=ReviewSerializer
    permission_classes=[IsReviewerOrReadOnly]
    


