from django.urls import path
from .views import UserSignupView, LoginView, ForgotPasswordView,ResetPasswordView  # Import both views

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('login/', LoginView.as_view(), name='login'),
]
