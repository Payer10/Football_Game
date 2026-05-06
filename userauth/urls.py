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
from .views import (
    RefreshTokenView, SignOutView, SignupView, ResendVerification, VerifyEmailView, 
    SignInViwe, ForgotPasswordView, VerificationResetCodeView, ResetPasswordView, UserDetailView,
    AdminSignInView, AdminSignOutView, AdminForgotPasswordView, AdminVerificationResetCodeView,
    AdminResetPasswordView, AdminRefreshTokenView, AdminUserDetailView
)

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
    path('user-detail/<uuid:user_id>/', UserDetailView.as_view(), name='user-detail'),

    # Admin Auth URLs
    path('admin/signin/', AdminSignInView.as_view(), name="admin-signin"),
    path('admin/signout/', AdminSignOutView.as_view(), name="admin-signout"),
    path('admin/forgot-email/', AdminForgotPasswordView.as_view(), name='admin-forgot-password'),
    path('admin/forgot-email-verify/', AdminVerificationResetCodeView.as_view(), name='admin-verify-forgot'),
    path('admin/reset-password/', AdminResetPasswordView.as_view(), name="admin-reset_password"),
    path('admin/refresh-token/', AdminRefreshTokenView.as_view(), name='admin-refresh_token'),
    path('admin/user-detail/<uuid:user_id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
]