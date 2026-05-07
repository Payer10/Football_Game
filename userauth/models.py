
# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     username = models.CharField(max_length=200)
#     email = models.EmailField(unique=True)
#     image = models.URLField()
#     jersey = models.IntegerField(default=0, null=True)
#     position = models.CharField(max_length=30, null=True)
#     tags = models.JSONField(default=list, null=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


#     def __str__(self):
#         return self.email





from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, AbstractUser, BaseUserManager
from django.utils import timezone
import uuid




# user manager create for create user and superuser
class UserManager(BaseUserManager):
    def create_user(self, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError("Email must be provided")
        email = self.normalize_email(email)
        if not username:
            username = ''  # placeholder, will be set after save
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        if not user.username or user.username == '':
            user.username = str(user.id).replace('-', '')[:16]
            user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # admin auto active
        extra_fields.setdefault('is_verified', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, username, password, **extra_fields)





# -----------custom user model----------
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True, blank=True)
    # phone_number = models.CharField(max_length=15)
    # phone_country_code = models.CharField(max_length=5)
    # full_name = models.CharField(max_length=255)



    # is_terms_service = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=50, default='user')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)


    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__ (self):
        return self.email



# -----------verification code model----------
class VarificationCode(models.Model):
    PURPOSE_CHOICES = [
        ('email_verification', 'Email Verification'),
        ('password_reset', 'Password Reset'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()
    secret_key = models.UUIDField(null=True, blank=True)

