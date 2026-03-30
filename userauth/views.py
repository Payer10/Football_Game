from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                'user': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=201)

        return Response(serializer.errors, status=400)
    

    

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email').strip().lower()
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)

                return Response({
                    'user': UserSerializer(user).data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=200)

            return Response({'error': 'Invalid credentials'}, status=400)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)