from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Task, TaskMember
from .serializers import UserSerializer, TaskSerializer, TaskMemberSerializer
from .utils import custom_response
from django.contrib.auth import authenticate
from rest_framework.response import Response




class RegisterUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return custom_response(success=True, message='User registered successfully', data=response.data, status=status.HTTP_201_CREATED)

class LoginUserAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return custom_response(success=False, message='Username and password are required', data=None, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            data = {'token': token.key}
            return custom_response(success=True, message='User logged in successfully', data=data)
        else:
            return custom_response(success=False, message='Unable to log in with provided credentials', data=None, status=status.HTTP_400_BAD_REQUEST)

class TaskListCreateAPIView(generics.ListCreateAPIView):
    
   
    permission_classes = [permissions.IsAuthenticated]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(success=True, message='Tasks retrieved successfully', data=serializer.data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return custom_response(success=True, message='Task created successfully', data=response.data, status=status.HTTP_201_CREATED)

    
class TaskDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return custom_response(success=True, message='Task retrieved successfully', data=response.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        return custom_response(success=True, message='Task updated successfully', data=response.data)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({ 'success': True,'message': 'Task deleted successfully'})

class TaskMemberAddRemoveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(username=request.data['username'])
        TaskMember.objects.get_or_create(task=task, user=user)
        return custom_response(success=True, message='Member added to task successfully')

    def delete(self, request, pk):
        task = Task.objects.get(pk=pk)
        user = User.objects.get(username=request.data['username'])
        TaskMember.objects.filter(task=task, user=user).delete()
        return Response({ 'success': True,'message': 'Member removed from task successfully'})

class TaskMemberListAPIView(generics.ListAPIView):
    serializer_class = TaskMemberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        task_id = self.kwargs['pk']
        return TaskMember.objects.filter(task__id=task_id)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return custom_response(success=True, message='Task members retrieved successfully', data=serializer.data)

class TaskStatusUpdateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        task = Task.objects.get(pk=pk)
        task.status = request.data['status']
        task.save()
        serializer = TaskSerializer(task)
        return custom_response(success=True, message='Task status updated successfully', data=serializer.data)
