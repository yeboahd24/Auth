from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from .serializers import CustomUserSerializer
from django.contrib.auth import authenticate


class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key})
        else:
            return Response(serializer.errors, status=400)


class UserLoginAPIView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        user = authenticate(username=email_or_phone, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)
