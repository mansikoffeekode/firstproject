from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from user.serializers import *
from rest_framework.views import APIView
from user.utils import send_reset_password_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode


# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return User.objects.all()


class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data['email'])
            if not user.check_password(request.data['password']):
                return Response({"password": "Password is wrong"}, status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_active:
                return Response({"is_active": "User is not active."}, status=status.HTTP_400_BAD_REQUEST)
            user.last_login = timezone.now()
            user.save()
            data = AuthenticateSerializer(user, context={'request': request}).data
            return Response(data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"email": "Email is not exists in our system"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email=request.data['email'])
            send_reset_password_mail(user)
            return Response({"email": "Please check your mail for get reset password link."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"email": "Email is not exists in our system"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetValidateTokenView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid UID"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)


class PasswordResetCompleteView(APIView):
    serializer_class = CompleteResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        try:
            uid = urlsafe_base64_decode(request.data['uidb64']).decode()
            user = User.objects.get(pk=uid)
            if not default_token_generator.check_token(user, request.data['token']):
                return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(request.data['new_password'])
            user.save()
            return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid UID.'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return User.objects.filter(is_superuser=False, is_staff=False)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()
