import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from tasks.models import Task, List
from django.utils import timezone
from rest_framework.test import APIClient


@pytest.fixture
def user(db) -> AbstractUser:
    return get_user_model().objects.create_user(
        username='testuser', email='test@example.com', password='testpass123'
        )

@pytest.fixture
def task_list(db, user:AbstractUser) -> List:
    return List.objects.create(title='test', user=user)

@pytest.fixture
def task(db, user:AbstractUser, task_list:List) -> Task:
    return Task.objects.create(
        title='test', 
        description='test description',
        user=user, 
        repeat=1,
        due_date=timezone.now().date(), 
        list=task_list
        )

@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def authenticated_client(api_client:APIClient, user:AbstractUser) -> APIClient:
    api_client.force_authenticate(user=user)
    return api_client