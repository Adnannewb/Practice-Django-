from rest_framework import serializers
from .models import Event,Registration


class RegistrationSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    class Meta:
        model=Registration
        fields=['id','event','registered_at','user']
        read_only_fields=['id','registered_at','user']
        
        
    def validate(self, attrs):
        request=self.context['request']
        user=request.user
        event=attrs['event']
        
        if self.instance is None:
            if Registration.objects.filter(user=user,event=event).exists():
                raise serializers.ValidationError('User Already registered.')
        if Registration.objects.filter(event=event).count() >= event.capacity:
            raise serializers.ValidationError("Event is already full.")
        
        return attrs
    
    def create(self, validated_data):
        
        request = self.context['request']
        validated_data['user'] = request.user
        return Registration.objects.create(**validated_data)
        
        