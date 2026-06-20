from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, MyDayTaskViewSet


router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('myday', MyDayTaskViewSet, basename='task-myday')

urlpatterns = [
    path('', include(router.urls))
]