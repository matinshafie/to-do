import pytest
from django.contrib.auth.models import AbstractUser
from tasks.models import List, Task
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

    def test_list_deletion_cascade_all_tasks(self, user:AbstractUser, task_list:List):
        task = Task.objects.create(
            title='test1',
            user=user,
            list=task_list,
        )
        task_id = task.id

        task_list.delete()

        assert not Task.objects.filter(id=task_id).exists()

    def test_user_deletion_cascade_all_lists(self, user:AbstractUser):
        lst = List.objects.create(title='list2', user=user)
        lst_id = lst.id


        user.delete()


        assert not List.objects.filter(id=lst_id).exists()