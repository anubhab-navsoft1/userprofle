from django.shortcuts import render
from .models import UserProfile
from .serializers import   UserSerializer, UserSignInSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
import json
# Create your views here.

class UserListView(generics.GenericAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        
        user = UserProfile.objects.all().values()
        username = User.objects.all().values("username")
        print("username ----", username)
        print("----------->>>>", user)
        data = []
        for i in user:
            print("--------ppp", i)
            reponse = {
                "id" : i['id'],
                "username" : i['user_id'],
            #     # "email" : i['email'],
                 "phone_number" : i['phone_number'],
                 "address" : i['address'],
                 "city ": i['city'],
                 "state" : i['state'],
                 "country" : i['conutry'],
            }
            data.append(reponse)
        return Response({"data" : data, "message" : "Fetched"}, status = status.HTTP_200_OK)
    
class UserRegisrationView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            error_messages = self.user_exists(serializer.validated_data)
            if error_messages:
                return Response({"error": error_messages}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = self.create_user(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def user_exists(self, validated_data):
        error_messages = []
        if User.objects.filter(email=validated_data['email']).exists():
            error_messages.append("Email already exists.")
        if UserProfile.objects.filter(phone_number=validated_data['phone_number']).exists():
            error_messages.append("Phone number already exists.")
        if User.objects.filter(username=validated_data['username']).exists():
            error_messages.append("Username already exists.")
        return error_messages
    
    def create_user(self, serializer):
        user = User.objects.create_user(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
            email=serializer.validated_data['email']
        )
        UserProfile.objects.create(
            user=user,
            phone_number=serializer.validated_data['phone_number'],
            address=serializer.validated_data['address'],
            city=serializer.validated_data['city'],
            state=serializer.validated_data['state'],
            conutry=serializer.validated_data['conutry']
        )
        return user

class UserSignInView(generics.GenericAPIView):
    serializer_class = UserSignInSerializer  
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile does not exist'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(user)  # Use UserSerializer to serialize user

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'profile': serializer.data  
        }, status=status.HTTP_200_OK)

# class UpdateUser(generics.UpdateAPIView):
#     queryset = UserProfile.objects.all()
#     serializer_class = UserSerializer
#     lookup_field = 'pk'

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
        

class DestroyById(generics.GenericAPIView):
        
    def delete(self, request, id):
        user = User.objects.filter(id = id)
        user.delete()
        return Response({"message" : "Delete"})

            
class DeleteAllUsersView(generics.GenericAPIView):
    queryset = User.objects.all() 

    def delete(self, request, *args, **kwargs):
        try:
            self.get_queryset().delete()  # Delete all users
            return Response({'message': 'All users deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
    
        
