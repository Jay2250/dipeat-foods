from rest_framework import generics, status
from django.contrib.auth.models import User
from .models import Profile, PasswordResetToken
from .serializers import UserSerializer, ProfileSerializer, PasswordResetRequestSerializer, PasswordResetResponseSerializer

from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.utils.crypto import get_random_string


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


@permission_classes([AllowAny])
class PasswordResetRequestView(generics.CreateAPIView):
    serializer_class = PasswordResetRequestSerializer

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User with this email does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = PasswordResetToken.objects.get_or_create(user=user)
        if not created:
            token.token = get_random_string(length=32)
            token.save()

        # Here, you can send the token to the user via another channel (e.g., SMS)
        # In this example, we'll return the token for simplicity
        return Response({'token': token.token}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class PasswordResetView(generics.CreateAPIView):
    serializer_class = PasswordResetResponseSerializer

    def create(self, request, *args, **kwargs):
        token = request.data.get('token')
        password = request.data.get('password')

        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response({'message': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_token.user
        user.set_password(password)
        user.save()

        reset_token.delete()

        return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)