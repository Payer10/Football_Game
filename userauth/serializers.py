from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'image', 'password','jersey', 'position', 'tags']
        read_only_fields = ['id', 'image']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializerCURD(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email','password', 'image', 'jersey', 'position', 'tags']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': False}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user