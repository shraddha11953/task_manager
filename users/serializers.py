from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from .models import Role


# ----------------------------------------
# REGISTER SERIALIZER
# ----------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        return user


# ----------------------------------------
# LOGIN SERIALIZER
# ----------------------------------------
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# ----------------------------------------
# ROLE SERIALIZER
# ----------------------------------------
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['user', 'role']
