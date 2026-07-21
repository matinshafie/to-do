from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, \
    ListModelMixin, DestroyModelMixin, UpdateModelMixin
from .serializers import TaskSerializer, ListSerializer, CompletedTaskSerializer
from .models import Task, List, CompletedTask
from django.utils import timezone

# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
        
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).select_related('list')
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)
    
class MyDayTaskViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, UpdateModelMixin, GenericViewSet
    ):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, due_date=timezone.now().date()).select_related('list')

    def perform_update(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)

class ListViewSet(ModelViewSet):
    serializer_class = ListSerializer
    
    def get_queryset(self):
        return List.objects.filter(user=self.request.user).prefetch_related('tasks')
    
    def perform_create(self, serializer:ListSerializer):
        serializer.save(user=self.request.user)

class TaskListViewSet(ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(
            user=self.request.user, 
            list_id=self.kwargs.get('list_pk')
            ).select_related('list')
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user, list_id=self.kwargs['list_pk'])

class CompletedTaskViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, GenericViewSet
    ):
    serializer_class = CompletedTaskSerializer

    def get_queryset(self):
        return CompletedTask.objects.filter(task__user=self.request.user).select_related('task')
    
class MyDayCompletedTaskViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, GenericViewSet
    ):
    serializer_class = CompletedTaskSerializer

    def get_queryset(self):
        return CompletedTask.objects.filter(
            task__user=self.request.user, completed_at__date=timezone.now().date()
            ).select_related('task')

class CompletedTaskListViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, GenericViewSet
    ):
    serializer_class = CompletedTaskSerializer

    def get_queryset(self):
        return CompletedTask.objects.filter(task__user=self.request.user, task__list_id=self.kwargs['list_pk'])