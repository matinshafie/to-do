from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import TaskViewSet, MyDayTaskViewSet, ListViewSet, TaskListViewSet


router = SimpleRouter()
router.register('tasks', TaskViewSet, basename='task')
router.register('myday', MyDayTaskViewSet, basename='task-myday')
router.register('lists', ListViewSet, basename='list')

lists_router = NestedSimpleRouter(router, 'lists', lookup='list')
lists_router.register('tasks', TaskListViewSet, basename='list-tasks')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(lists_router.urls))
]