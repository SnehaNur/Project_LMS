from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from datetime import timedelta
import random


class CustomUser(AbstractUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    contact_number = models.CharField(
        validators=[phone_regex],
        max_length=15,
        unique=True
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)

    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'contact_number']

    def __str__(self):
        return self.username
    
User = get_user_model()

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    @classmethod
    def create_otp(cls, user):
        # Delete any existing OTPs for this user
        cls.objects.filter(user=user).delete()
        
        # Generate 6-digit OTP
        otp = str(random.randint(100000, 999999))
        expires_at = timezone.now() + timedelta(minutes=5)
        
        return cls.objects.create(
            user=user,
            otp=otp,
            expires_at=expires_at
        )

    @classmethod
    def validate_otp(cls, email, otp_code):
        try:
            user = User.objects.get(email=email)
            return cls.objects.get(
                user=user,
                otp=otp_code,
                is_used=False,
                expires_at__gt=timezone.now()
            )
        except (User.DoesNotExist, cls.DoesNotExist):
            return None

    def mark_as_used(self):
        self.is_used = True
        self.save()
        
    @classmethod
    def find_valid_otp(cls, otp_code):
        return cls.objects.filter(
            otp=otp_code,
            is_used=False,
            expires_at__gt=timezone.now()
        ).first()