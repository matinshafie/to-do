import pytest
from django.contrib.auth.models import AbstractUser
from rest_framework.test import APIClient
from tasks.models import List, Task
from rest_framework import status


pytest.mark.django_db
class TestTaskViewSet:
    def test_list_tasks_authenticated_user(self, user:AbstractUser, api_client:APIClient):
        task = Task.objects.create(title='task1', user=user)

        response = api_client.get(path='/tasks/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED