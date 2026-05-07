# from .models import User
# from rest_framework import serializers


# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'image', 'password','jersey', 'position', 'tags']
#         read_only_fields = ['id', 'image']

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user


# class UserSerializerCURD(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email','password', 'image', 'jersey', 'position', 'tags']
#         read_only_fields = ['id']
#         extra_kwargs = {
#             'password': {'write_only': True},
#             'username': {'required': False}
#         }


#     def create(self, validated_data):
#         username = validated_data.get('username')
        
#         if not username:
#             raise serializers.ValidationError({
#                 "username": "This field is required."
#             })

#         user = User(
#             username=username,
#             email=validated_data.get('email')
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user





from rest_framework import serializers
from .models import User

# -----------sign up serializer----------
class SignUpSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'email',
            'username',
            'password',
        ]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username', None)
        user = User.objects.create_user(
            email=validated_data['email'],
            username=username,
            password=password,
        )
        return user


# -----------update username serializer----------
class UpdateUserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]



# -----------user profile serializer----------
class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture']



# -----------sign in serializer----------
class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    # phone_number = serializers.CharField(required=False)




    def validate(self, data):
        user = None
        if data.get('email'):
            user = User.objects.filter(email=data['email']).first()
        if data.get('username'):
            user = User.objects.filter(username=data['username']).first()

        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_verified:
            raise serializers.ValidationError("User is not verified")
        
        # if data.get('phone_number'):
        #     user = User.objects.filter(phone_number=data['phone_number']).first()

        
        return user



# -----------sign out serializer----------
class SignOutSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


# -----------refresh token serializer----------
class RefreshTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()




class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'is_active', 'is_verified', 'role', 'created_at']
        read_only_fields = ['email', 'created_at', 'is_active', 'is_verified', 'role']

# -----------admin sign in serializer----------
class AdminSignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = None
        if data.get('email'):
            user = User.objects.filter(email=data['email']).first()
        if data.get('username'):
            user = User.objects.filter(username=data['username']).first()

        if not user or not user.check_password(data['password']):
            raise serializers.ValidationError("Invalid credentials")
        
        if not user.is_verified:
            raise serializers.ValidationError("User is not verified")
            
        if user.role != 'admin':
            raise serializers.ValidationError("Only admins are allowed to sign in here")
        
        return user