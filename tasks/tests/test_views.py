import pytest
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient
from tasks.models import List, Task
from rest_framework import status


pytest.mark.django_db
class TestTaskViewSet:
    def test_list_tasks_unauthenticated_user(self, user:AbstractUser, api_client:APIClient):
        task = Task.objects.create(title='test unautherized', user=user)

        response = api_client.get(path='/tasks/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_tasks_isolation_by_user(
            self, authenticated_client:APIClient, user:AbstractUser, other_user:AbstractUser
            ):
        task_user = Task.objects.create(title='isolation task', user=user)
        task_user = Task.objects.create(title='isolation task other user', user=other_user)

        response = authenticated_client.get('/tasks/')

        assert len(response.data) == 1