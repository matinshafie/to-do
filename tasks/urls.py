from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, MyDayTaskViewSet, ListViewSet


router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('myday', MyDayTaskViewSet, basename='task-myday')
router.register('lists', ListViewSet, basename='list')

urlpatterns = [
    path('', include(router.urls))
]