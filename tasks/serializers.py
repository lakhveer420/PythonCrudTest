from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task, TaskMember

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'], 
            email=validated_data['email']
        )
        user.set_password(validated_data['password']) 
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'created_at', 'updated_at']

class TaskMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = TaskMember
        fields = ['id', 'task', 'user']
