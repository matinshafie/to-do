from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, \
    ListModelMixin, DestroyModelMixin, UpdateModelMixin
from .serializers import TaskSerializer, ListSerializer
from .models import Task, List
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
        return Task.objects.filter(user=self.request.user, due_date=timezone.localdate()).select_related('list')
    
    def perform_create(self, serializer:TaskSerializer):
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
        serializer.save(user=self.request.user, list_id=self.kwargs.get('list_pk'))