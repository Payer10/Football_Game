# from django.shortcuts import render
# from django.http import JsonResponse
# from .models import User
# from .serializers import UserSerializer, UserSerializerCURD
# from rest_framework.views import APIView
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.response import Response
# from rest_framework import status

# from rest_framework_simplejwt.tokens import RefreshToken

# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)

#         if serializer.is_valid():
#             user = serializer.save()

#             refresh = RefreshToken.for_user(user)

#             return Response({
#                 'user': serializer.data,
#                 'refresh': str(refresh),
#                 'access': str(refresh.access_token),
#             }, status=201)

#         return Response(serializer.errors, status=400)
    

    

# class LoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email').strip().lower()
#         password = request.data.get('password')

#         try:
#             user = User.objects.get(email=email)

#             if user.check_password(password):
#                 refresh = RefreshToken.for_user(user)

#                 return Response({
#                     'user': UserSerializer(user).data,
#                     'refresh': str(refresh),
#                     'access': str(refresh.access_token),
#                 }, status=200)

#             return Response({'error': 'Invalid credentials'}, status=400)

#         except User.DoesNotExist:
#             return Response({'error': 'User not found'}, status=404)
        


# class UserDetailView(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializerCURD
#     http_method_names = ['get', 'put', 'patch', 'delete', 'post']





from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    SignUpSerializer, SignInSerializer, SignOutSerializer, RefreshTokenSerializer,
    UserProfileSerializer, UpdateProfileSerializer, UserDetailSerializer,
    AdminSignInSerializer,
)
from .models import User, VarificationCode
from .utils import generate_verification_code, get_expiration_time
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
import uuid
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework.permissions import IsAuthenticated, AllowAny


# ----------sign up view----------
class SignupView(GenericAPIView):
    serializer_class = SignUpSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        otp = generate_verification_code()

        send_mail(
            subject='Email Verification Code', 
            message=f'{otp} is your verification code',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )

        VarificationCode.objects.create(
            user=user,
            code=otp,
            purpose='email_verification',
            expired_at=get_expiration_time()
        )
    
        return Response({"user_id": str(user.id)}, status=201)



# ----------app config view----------
class AppConfigView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            "version": "12.12.3",
            "verify_email": True
        })


# ----------resend verification code view----------
class ResendVerification(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        user = User.objects.filter(id=request.data.get('user_id')).first()
        if not user:
            return Response({"message": "User not found"}, status=404)
        
        otp = generate_verification_code()

        send_mail(
            subject='Email Verification Code', 
            message=f'{otp} is your verification code',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        
        VarificationCode.objects.create(
            user=user,
            code=otp,
            purpose='email_verification',
            expired_at=get_expiration_time()
        )
        return Response({'message': 'verification code sent to your email'}, status=200)


# ----------verify email view----------
class VerifyEmailView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({'message': 'invalid email or otp'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'invalid email or otp'}, status=400)
        
        otp = VarificationCode.objects.filter(
            user=user,
            code=otp_code,
            purpose='email_verification',
            expired_at__gte=now()
        ).last()

        if not otp:
            return Response({'message': 'invalid email or otp'}, status=400)

        user.is_verified = True
        user.save()
        otp.delete()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'access_token_valid_till': int((now() + refresh.access_token.lifetime).timestamp() * 1000),
            'refresh_token': str(refresh),
            'user_id': str(user.id),
            'user_role': user.role
        })




# ----------sign in view----------
class SignInViwe(GenericAPIView):
    serializer_class = SignInSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Extract the custom error message from serializer errors
            errors = serializer.errors
            if 'non_field_errors' in errors:
                for err in errors['non_field_errors']:
                    # Check if it's our custom dict error
                    if isinstance(err, dict):
                        return Response(err, status=400)
                    try:
                        import json
                        err_dict = json.loads(str(err).replace("'", '"'))
                        return Response(err_dict, status=400)
                    except:
                        pass
            return Response({"message": "invalid email or password"}, status=400)

        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'access_token_valid_till': int((now() + refresh.access_token.lifetime).timestamp() * 1000),
            'refresh_token': str(refresh),
            'user_id': str(user.id),
            'user_role': user.role
        })
    


# ----------sign out view----------
class SignOutView(GenericAPIView):
    serializer_class = SignOutSerializer
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        tokens = OutstandingToken.objects.filter(user_id=user_id)

        if not tokens.exists():
            return Response({'error': 'No active session found'}, status=404)

        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

        return Response({'message': 'Successfully signed out'}, status=204)



# ----------forgot password view----------
class ForgotPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'message': 'invalid email or otp'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'invalid email or otp'}, status=400)
        
        otp = generate_verification_code()
        send_mail(
            subject='Password Reset Verification Code',
            message=f'{otp} is your password reset verification code',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        code = VarificationCode.objects.create(
            user=user,
            code=otp,
            purpose="password_reset",
            expired_at=get_expiration_time()
        )

        return Response({
            "user_id": str(user.id),
            "expires_at": int(code.expired_at.timestamp() * 1000)
        })


# ----------forget password verify view----------
class ForgetPasswordVerifyView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')

        if not email or not otp_code:
            return Response({'message': 'invalid email or otp'}, status=400)

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({'message': 'invalid email or otp'}, status=400)

        otp = VarificationCode.objects.filter(
            user=user,
            code=otp_code,
            purpose='password_reset',
            expired_at__gte=now()
        ).last()

        if not otp:
            return Response({'message': 'invalid email or otp'}, status=400)

        otp.delete()
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'access_token_valid_till': int((now() + refresh.access_token.lifetime).timestamp() * 1000),
            'refresh_token': str(refresh),
            'user_id': str(user.id),
            'user_role': user.role
        })




# ----------reset password view----------
class ResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.get(id=request.data.get('user_id'))
        
        otp = VarificationCode.objects.filter(
            user = user,
            purpose = 'password_reset',
            secret_key = request.data.get('secret_key')
        ).last()

        if not otp:
            return Response({'error': 'Invalid secret_key'})
        user.set_password(request.data.get('password'))
        user.save()
        otp.delete

        return Response({'message': 'success your reset password'},status=202)
    


# ---------------refresh token view----------
class RefreshTokenView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    authentication_classes = []
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data['user_id']

        token = OutstandingToken.objects.filter(user_id=user_id).order_by('-created_at').first()

        if not token:
            return Response({'error': 'No active refresh token found'}, status=404)

        refresh = RefreshToken(token.token)

        return Response({
            'access_token': str(refresh.access_token),
            'access_token_valid_till': int((now()+refresh.access_token.lifetime).timestamp()*1000)
        })
    

# ----------profile view----------
class ProfileView(GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# ----------update profile view----------
class UpdateProfileView(GenericAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ----------user detail view (legacy)----------
class UserDetailView(GenericAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return Response({'message': 'User not found'}, status=404)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# ==========================================
#              ADMIN Auth Views
# ==========================================

class AdminSignInView(GenericAPIView):
    serializer_class = AdminSignInSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=400)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'access_token_valid_till': int((now()+ refresh.access_token.lifetime).timestamp() * 1000),
            'refresh_token': str(refresh),
            'user_id': str(user.id),
            'user_role': user.role
        })

class AdminSignOutView(SignOutView):
    pass

class AdminForgotPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user = (User.objects.filter(email=request.data.get('email'), role='admin').first() or
                User.objects.filter(phone_number=request.data.get('phone_number'), role='admin').first() or
                User.objects.filter(username=request.data.get('username'), role='admin').first())
        if not user:
            return Response({'error': 'Invalid admin user details'}, status=404)
        
        otp = generate_verification_code()
        send_mail(
            subject='this code is your admin forgot password verificaiton code',
            message=f'{otp} is your admin forgot password varification code',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        code = VarificationCode.objects.create(
            user= user,
            code= otp,
            purpose= "password_reset",
            expired_at= get_expiration_time()
        )

        return Response({
            "user_id": str(user.id),
            "expires_at": int(code.expired_at.timestamp() * 1000)
        })

class AdminVerificationResetCodeView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(id=request.data.get('user_id'), role='admin')
        except User.DoesNotExist:
            return Response({'error': 'Invalid admin user_id'}, status=404)

        otp = VarificationCode.objects.filter(
            user=user,
            code=request.data.get('verification_code'),
            purpose='password_reset',
            expired_at__gte=now()
        ).last()
        if not otp:
            return Response({'error': 'Invalid or expired code'}, status=404)
            
        otp.secret_key = uuid.uuid4()
        otp.save()

        return Response({
            "secret_key": str(otp.secret_key)
        })

class AdminResetPasswordView(GenericAPIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            user = User.objects.get(id=request.data.get('user_id'), role='admin')
        except User.DoesNotExist:
            return Response({'error': 'Invalid admin user_id'}, status=404)
        
        otp = VarificationCode.objects.filter(
            user = user,
            purpose = 'password_reset',
            secret_key = request.data.get('secret_key')
        ).last()

        if not otp:
            return Response({'error': 'Invalid secret_key'}, status=400)
            
        user.set_password(request.data.get('password'))
        user.save()
        otp.delete()

        return Response({'message': 'success your reset password'}, status=202)

class AdminRefreshTokenView(RefreshTokenView):
    pass

class AdminUserDetailView(UserDetailView):
    def get(self, request, user_id):
        user = User.objects.filter(id=user_id, role='admin').first()
        if not user:
            return Response({'error': 'Admin User not found'}, status=404)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)