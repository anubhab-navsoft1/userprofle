from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()
    phone_number = serializers.CharField()
    address = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    conutry = serializers.CharField()
    
    def update(self, instance, validated_data):
        # Update UserProfile instance fields
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.address = validated_data.get('address', instance.address)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.conutry = validated_data.get('conutry', instance.conutry)
        instance.save()

        # Update associated User instance fields
        user_data = validated_data.pop('user', {})  # Extract user data
        user = instance.user
        user.username = user_data.get('username', user.username)
        user.password = user_data.get('password', user.password)
        user.email = user_data.get('email', user.email)
        user.save()

        return instance
    
class UserSignInSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.CharField()