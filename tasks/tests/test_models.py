import pytest
from django.contrib.auth.models import AbstractUser
from tasks.models import List
from uuid import UUID
from django.utils import timezone


@pytest.mark.django_db
class TestListModel:
    def test_list_creation(self, user:AbstractUser):
        list_obj = List.objects.create(title='list1', user=user)

        assert list_obj.title == 'list1'
        assert list_obj.user == user
        assert isinstance(list_obj.id, UUID)
        assert list_obj.created_at is not None

    def test_list_auto_now_add_created_at(self, user:AbstractUser):
        before = timezone.now()
        list_obj = List.objects.create(title='list2', user=user)
        after = timezone.now()

        assert before <= list_obj.created_at <= after