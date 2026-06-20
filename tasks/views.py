from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import RetrieveModelMixin, \
    ListModelMixin, DestroyModelMixin, UpdateModelMixin
from .serializers import TaskSerializer, CreateTaskSerializer, MyDayTaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated
from datetime import date

# Create your views here.
class TaskViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer
        
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateTaskSerializer
        return TaskSerializer
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)
    
class MyDayTaskViewSet(
    RetrieveModelMixin, ListModelMixin, 
    DestroyModelMixin, UpdateModelMixin, GenericViewSet
    ):
    permission_classes = [IsAuthenticated]
    serializer_class = MyDayTaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).filter(due_date=date.today())
    
    def perform_create(self, serializer:TaskSerializer):
        serializer.save(user=self.request.user)