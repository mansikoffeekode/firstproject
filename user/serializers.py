from django.contrib.auth import password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from user.models import User


class AuthenticateSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'dob', 'is_active', 'is_superuser', 'is_staff', 'last_login', 'date_joined',
                  'token']

    def get_token(self, instance):
        token = RefreshToken.for_user(self.instance).access_token
        return str(token)


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'password']

    def validate_email(self, value):
        if User.objects.filter(email__icontains=value).exists():
            raise serializers.ValidationError("This email is already register!")
        return value

    def validate(self, attrs):
        try:
            password_validation.validate_password(attrs['password'])
        except Exception as e:
            raise serializers.ValidationError(e)
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'],
                                        name=validated_data['name'],
                                        password=validated_data['password'])
        return user

    def to_representation(self, instance):
        data = AuthenticateSerializer(instance, context=self.context).data
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class CompleteResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    new_password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)
    confirm_password = serializers.CharField(style={'input_type': 'password'}, required=True, write_only=True)

    def validate(self, data):
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Your old password is wrong.'})

        if data.get('confirm_password') != data.get('new_password'):
            raise serializers.ValidationError({'password': 'Both password must be same.'})
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(style={'input_type': 'password'}, required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'dob', 'is_active', 'date_joined']
