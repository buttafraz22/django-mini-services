from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import os
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        # Validate the data
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_403_FORBIDDEN)

        # Save the object in the database
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def get(self, request):
        email = request.data['email']
        password = request.data['password']
        
        # Filter the objects from database
        user = User.objects.filter(email=email).first()

        # Handle Guard clauses
        if user is None:
            return Response({"message": "No such User with email exists"}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.check_password(password):
            return Response({"message": "Incorrect Password"}, status=status.HTTP_403_FORBIDDEN)
        
        # Define the payload
        payload={
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), # Validate the token for 60 minutes
            'iat': datetime.datetime.utcnow()
        }

        # Make the token
        token = jwt.encode(payload, os.environ['JWT_SECRET'], algorithm='HS256')
        
        response =  Response(status=status.HTTP_202_ACCEPTED)
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
                            "jwt": token
                        }

        return response

class UserView(APIView):
    def get(self, request):
        auth_header = request.headers.get('Authorization')
        
        # Check if the Authorization header exists and if it starts with 'Bearer '
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        token = auth_header.split(' ')[1]

        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            payload=jwt.decode(token, os.environ['JWT_SECRET'], algorithms=['HS256'])
            
        except:
            return Response(data={"message": "Error in Decoding the Payload"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        user = User.objects.filter(id=payload['id']).first()
        print(user.email)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)
