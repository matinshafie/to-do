from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, \
    ListModelMixin, DestroyModelMixin, UpdateModelMixin
from .serializers import TaskSerializer, CreateTaskSerializer, UpdateTaskSerializer, ListSerializer
from .models import Task, List
from django.utils import timezone

# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
        
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, list=None)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTaskSerializer
        return TaskSerializer
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)
    
class MyDayTaskViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, UpdateModelMixin, GenericViewSet
    ):

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, due_date=timezone.localdate())
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return UpdateTaskSerializer
        return TaskSerializer
    

class ListViewSet(ModelViewSet):
    serializer_class = ListSerializer
    
    def get_queryset(self):
        return List.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer:ListSerializer):
        serializer.save(user=self.request.user)

class TaskListViewSet(ModelViewSet):
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, list_id=self.kwargs.get('list_pk'))
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        elif self.action in ['update', 'partial_update']:
            return UpdateTaskSerializer
        return TaskSerializer
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)