from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer, CreateTaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated

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