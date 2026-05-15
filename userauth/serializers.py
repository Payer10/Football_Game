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
            'name',
            'email',
            'username',
            'password',
        ]
        extra_kwargs = {
            'username': {'required': False, 'allow_blank': True},
            'name': {'required': True},
        }

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        if value and User.objects.filter(username=value).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        username = validated_data.pop('username', None)
        name = validated_data.pop('name', '')
        user = User.objects.create_user(
            email=validated_data['email'],
            username=username,
            name=name,
            password=password,
        )
        return user


# -----------sign in serializer----------
class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)


# -----------sign out serializer----------
class SignOutSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


# -----------refresh token serializer----------
class RefreshTokenSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()


# -----------user profile serializer----------
class UserProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source='role', read_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'image', 'username', 'user_role']
        read_only_fields = ['name', 'email', 'image', 'username', 'user_role']


# -----------update profile serializer----------
class UpdateProfileSerializer(serializers.ModelSerializer):
    user_role = serializers.CharField(source='role', read_only=True)

    class Meta:
        model = User
        fields = ['name', 'email', 'image', 'username', 'user_role']
        read_only_fields = ['user_role']
        extra_kwargs = {
            'name': {'required': False},
            'email': {'required': False},
            'image': {'required': False},
            'username': {'required': False},
        }

    def validate_email(self, value):
        if self.instance and User.objects.filter(email=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("email already exists")
        return value

    def validate_username(self, value):
        if self.instance and User.objects.filter(username=value).exclude(id=self.instance.id).exists():
            raise serializers.ValidationError("username already exists")
        return value

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            if value is not None:
                setattr(instance, field, value)
        instance.save()
        return instance


# -----------user detail serializer----------
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