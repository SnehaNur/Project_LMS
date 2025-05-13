from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'contact_number',
            'email',
            'username',
            'password'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            contact_number=validated_data['contact_number']
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()  # Changed from email to username
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate_username(self, value):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this username does not exist.")
        return value

class ResetPasswordSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return data

'''  
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        # Check password match
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        
        # Validate password strength
        try:
            validate_password(data['new_password'])
        except ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        
        return data
'''