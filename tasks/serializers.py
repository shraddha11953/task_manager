from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

# ----------------------------------------
# USER SERIALIZER
# ----------------------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# ----------------------------------------
# TASK SERIALIZER (Full Detail)
# ----------------------------------------
class TaskSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'is_completed',   # <-- use is_completed
            'owner',
            'created_at',
            'updated_at'
        ]

# ----------------------------------------
# TASK CREATE/UPDATE SERIALIZER
# ----------------------------------------
class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'title',
            'description',
            'is_completed',   # <-- use is_completed
        ]
