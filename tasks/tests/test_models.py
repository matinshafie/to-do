import pytest
from django.contrib.auth.models import AbstractUser
from tasks.models import List
from uuid import UUID


@pytest.mark.django_db
class TestListModel:
    def test_list_creation(self, user:AbstractUser):
        list_obj = List.objects.create(title='test', user=user)

        assert list_obj.title == 'test'
        assert list_obj.user == user
        assert isinstance(list_obj.id, UUID)
        assert list_obj.created_at is not None