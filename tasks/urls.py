from django.urls import path
from .views import RegisterUserAPIView, LoginUserAPIView, TaskListCreateAPIView, TaskDetailAPIView, TaskMemberAddRemoveAPIView, TaskMemberListAPIView, TaskStatusUpdateAPIView



urlpatterns = [
   
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('login/', LoginUserAPIView.as_view(), name='login'),
    path('create-task/', TaskListCreateAPIView.as_view(), name='create-task'),
    path('list-task/', TaskListCreateAPIView.as_view(), name='list-task'),
    path('detail-task/<int:pk>/', TaskDetailAPIView.as_view(), name='detail-task'),
    path('update-task/<int:pk>/', TaskDetailAPIView.as_view(), name='update-task'),
    path('delete-task/<int:pk>/', TaskDetailAPIView.as_view(), name='delete-task'),

    #TASK MEMBERS APIS
    path('tasks/members/list/<int:pk>/', TaskMemberListAPIView.as_view(), name='task-member-list'),
    path('tasks/members/add/<int:pk>/', TaskMemberAddRemoveAPIView.as_view(), name='task-member-add'),
    path('tasks/members/remove/<int:pk>/', TaskMemberAddRemoveAPIView.as_view(), name='task-member-remove'),
    path('tasks/status/<int:pk>/', TaskStatusUpdateAPIView.as_view(), name='task-status-update'),
]
