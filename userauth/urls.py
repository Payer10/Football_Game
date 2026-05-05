# from django.urls import path
# from .views import RegisterView, LoginView , UserDetailView
# from rest_framework.routers import DefaultRouter


# router = DefaultRouter()
# router.register(r'users', UserDetailView)

# urlpatterns = [
#     path('register/', RegisterView.as_view(), name='register'),
#     path('login/', LoginView.as_view(), name='login'),
# ] + router.urls



from django.urls import path
from .views import RefreshTokenView, SignOutView, SignupView, ResendVerification, VerifyEmailView, SignInViwe, ForgotPasswordView, VerificationResetCodeView, ResetPasswordView, UserDetailView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('resend-verification/', ResendVerification.as_view(), name='resend_verification'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('signin/', SignInViwe.as_view(), name="user-signin"),
    path('signout/', SignOutView.as_view(), name="user-signout"),
    path('forgot-email/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('forgot-email-verify/', VerificationResetCodeView.as_view(), name='verify-forgot'),
    path('reset-password/', ResetPasswordView.as_view(), name="reset_password"),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh_token'),
    path('user-detail/', UserDetailView.as_view(), name='user-detail'),
]