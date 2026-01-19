from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Importación para manejar los Tokens JWT
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

# --- TUS VISTAS ABAJO ---

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

@api_view(['POST'])
def login_usuario(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generamos los tokens JWT para el usuario
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login exitoso",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)
    else:
        return Response(
            {"error": "Credenciales inválidas"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

# Vista de prueba para el Interceptor de Angular
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil_usuario(request):
    return Response({
        "username": request.user.username,
        "message": "Si ves esto, tu interceptor envió el token correctamente"
    })