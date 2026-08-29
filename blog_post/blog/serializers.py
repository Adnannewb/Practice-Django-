from .models import Post,Comment
from rest_framework import serializers
from django.contrib.auth.models import User

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model=Post
        fields=['id','title','content','is_published']

class CommentSerializer(serializers.ModelSerializer):
    commentator=serializers.StringRelatedField(read_only=True)
    class Meta:
        model=Comment
        fields=['id','post','comment','commentator','created_at']
        
    def validate_comment(self, value):
        if not value or value.strip() == "":
            raise serializers.ValidationError('Empty Comment is not allowed!')
        return value
            
    
    