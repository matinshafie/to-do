from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer: TaskSerializer):
        return serializer.save(user=self.request.user)