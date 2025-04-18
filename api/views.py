from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAdmin, IsPremium, IsCliente
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    AuthUserRegistrationSerializer,
    AuthUserLoginSerializer,
    UserSerializer
)

from .models import User,Role


class AuthUserRegistrationView(APIView):
    serializer_class = AuthUserRegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save()
            status_code = status.HTTP_201_CREATED

            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User successfully registered!',
                'user': serializer.data
            }

            return Response(response, status=status_code)


class AuthUserLoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = AuthUserLoginSerializer

    def post(self, request):
        
        print("LoginView ejecutado - Se recibió una solicitud de login del usuario:", request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)



        return Response({
            'success': True,
            'message': 'Login exitoso',
            'data': serializer.validated_data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    #permission_classes = [IsAuthenticated]  

    def post(self, request):
        #print("LogoutView ejecutado - Se recibió una solicitud de logout del usuario:", request.user.email)
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class AllAccessView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return Response("Contenido público - TODOS pueden acceder.")

class PremiumView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsPremium]

    def get(self, request):
        return Response("Contenido exclusivo para CLIENTE PREMIUM.")

class ClienteView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsCliente]

    def get(self, request):
        return Response("Contenido exclusivo para CLIENTE.")

class AdminView(APIView):
    #permission_classes = [IsAuthenticated]
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response("Contenido exclusivo para ADMIN.")
    
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    #serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uid'

    def get_serializer_class(self):
        if self.action == 'create':
            return AuthUserRegistrationSerializer
        return UserSerializer

    def perform_create(self, serializer):
        current_user = self.request.user.email
        instance = serializer.save()
        instance.created_by = current_user
        instance.modified_by = current_user
        instance.save()

    def perform_update(self, serializer):
        serializer.save(modified_by=self.request.user.email)