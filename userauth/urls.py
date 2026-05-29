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
    SignInViwe, ForgotPasswordView, ForgetPasswordVerifyView, ResetPasswordView,
    UserDetailView, ProfileView, UpdateProfileView, AppConfigView,
    AdminSignInView, AdminSignOutView, AdminForgotPasswordView, AdminVerificationResetCodeView,
    AdminResetPasswordView, AdminRefreshTokenView, AdminUserDetailView,
    AdminBusinessSetupView, AdminBusinessSetupUpdateView
)

urlpatterns = [
    # User Auth URLs
    path('user/register', SignupView.as_view(), name='register'),
    path('user/login', SignInViwe.as_view(), name='login'),
    path('user/config', AppConfigView.as_view(), name='app-config'),
    path('user/verify-email', VerifyEmailView.as_view(), name='verify-email'),
    path('user/forget-password', ForgotPasswordView.as_view(), name='forget-password'),
    path('user/forget-password-verify', ForgetPasswordVerifyView.as_view(), name='forget-password-verify'),
    path('user/profile', ProfileView.as_view(), name='user-profile'),
    path('user/update-profile', UpdateProfileView.as_view(), name='update-profile'),
    # Kept endpoints (not in new spec but still useful)
    path('user/resend-verification', ResendVerification.as_view(), name='resend-verification'),
    path('user/signout', SignOutView.as_view(), name='user-signout'),
    path('user/reset-password', ResetPasswordView.as_view(), name='reset-password'),
    path('user/refresh-token', RefreshTokenView.as_view(), name='refresh-token'),
    path('user-detail/<uuid:user_id>', UserDetailView.as_view(), name='user-detail'),

    # Admin Auth URLs
    path('admin/signin/', AdminSignInView.as_view(), name="admin-signin"),
    path('admin/signout/', AdminSignOutView.as_view(), name="admin-signout"),
    path('admin/forgot-email/', AdminForgotPasswordView.as_view(), name='admin-forgot-password'),
    path('admin/forgot-email-verify/', AdminVerificationResetCodeView.as_view(), name='admin-verify-forgot'),
    path('admin/reset-password/', AdminResetPasswordView.as_view(), name="admin-reset_password"),
    path('admin/refresh-token/', AdminRefreshTokenView.as_view(), name='admin-refresh_token'),
    path('admin/admin-detail/<uuid:user_id>/', AdminUserDetailView.as_view(), name='admin-user-detail'),
    path('admin/business-setup/', AdminBusinessSetupView.as_view(), name='admin-business-setup'),
    path('admin/business-setup-update/', AdminBusinessSetupUpdateView.as_view(), name='admin-business-setup-update'),
]