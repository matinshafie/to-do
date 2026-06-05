from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task

# Create your views here.
class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()