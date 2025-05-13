from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator
from .serializers import LoginSerializer, UserSerializer  # Make sure both are imported
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail
from django.conf import settings
from .serializers import ForgotPasswordSerializer
from django.contrib.auth import get_user_model
from .models import PasswordResetOTP
from smtplib import SMTPAuthenticationError, SMTPException
from .serializers import ResetPasswordSerializer
from django.utils import timezone

class UserSignupView(CreateAPIView):
    serializer_class = UserSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "message": "User created successfully",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED,
            headers=headers
        )
    
class LoginView(GenericAPIView):  # 👈 change here
    serializer_class = LoginSerializer  # 👈 add this line
#class LoginView(APIView):
    @method_decorator(ratelimit(key='ip', rate='5/hour', method='POST'))
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username,
            'id': user.id,
            'is_admin': user.is_superuser,
        }, status=status.HTTP_200_OK)


User = get_user_model()

class ForgotPasswordView(GenericAPIView):
    serializer_class = ForgotPasswordSerializer  # Enables DRF UI form

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=serializer.validated_data['username'])
            otp_record = PasswordResetOTP.create_otp(user)
            
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp_record.otp}\nValid for 2 minutes. Do not share your OTP verification code with anyone.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return Response(
                {"message": "OTP has been sent to your registered email"},
                status=status.HTTP_200_OK
            )
            
        except User.DoesNotExist:
            return Response(
                {"error": "User with this username does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except SMTPAuthenticationError:
            return Response(
                {"error": "Email service authentication failed"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except SMTPException as e:
            return Response(
                {"error": f"Email sending failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

User = get_user_model()
class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        otp_code = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        # Find OTP record (modify this query based on your needs)
        try:
            otp_record = PasswordResetOTP.objects.get(
                otp=otp_code,
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except PasswordResetOTP.DoesNotExist:
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update user password
        user = otp_record.user
        user.set_password(new_password)
        user.save()

        # Mark OTP as used
        otp_record.is_used = True
        otp_record.save()

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK
        )


'''
class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp']
        new_password = serializer.validated_data['new_password']

        # Verify OTP
        otp_record = PasswordResetOTP.validate_otp(email, otp_code)
        if not otp_record:
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update user password
        user = otp_record.user
        user.set_password(new_password)
        user.save()

        # Mark OTP as used
        otp_record.is_used = True
        otp_record.save()

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK
        )
'''