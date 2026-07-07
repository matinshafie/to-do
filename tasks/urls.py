from django.urls import path, include
from rest_framework_nested.routers import SimpleRouter, NestedSimpleRouter
from .views import (TaskViewSet, 
                    MyDayTaskViewSet, 
                    ListViewSet, 
                    TaskListViewSet, 
                    CompletedTaskViewSet, 
                    MyDayCompletedTaskViewSet,
                    CompletedTaskListViewSet,
                    )


router = SimpleRouter()
router.register('inbox/tasks', TaskViewSet, basename='task')
router.register('inbox/completed', CompletedTaskViewSet, basename='completed-task')
router.register('myday/tasks', MyDayTaskViewSet, basename='task-myday')
router.register('myday/completed', MyDayCompletedTaskViewSet, basename='completed-task-myday')
router.register('lists', ListViewSet, basename='list')

lists_router = NestedSimpleRouter(router, 'lists', lookup='list')
lists_router.register('tasks', TaskListViewSet, basename='list-tasks')
lists_router.register('completed', CompletedTaskListViewSet, basename='list-completed')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(lists_router.urls))
]