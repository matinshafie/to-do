from rest_framework import serializers
from .models import Task, List, CompletedTask
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    list_title = serializers.SerializerMethodField('get_list_title')
    skip = serializers.BooleanField(write_only=True, required=False, default=False)

    class Meta:
        model = Task
        fields = 'id', 'title', 'description', 'created_at', 'completed', 'repeat', 'due_date', 'list_title', 'skip'

    def get_list_title(self, task:Task) -> str | None:
        return task.list.title if task.list else None

    def get_fields(self) -> dict[str, Task]:
        fields = super().get_fields()
        request = self.context.get('request')

        if not request:
            return fields

        if request.method == 'POST':
            fields.pop('completed', None)
            fields.pop('skip', None)
        

        elif request.method in ('PUT', 'PATCH'):
            fields.pop('user', None)

            instance = self.instance
            can_skip = (
                instance is not None 
                and instance.repeat 
                and instance.due_date
                and instance.due_date < timezone.localdate()
                )
            if not can_skip:
                fields.pop('skip', None)

        return fields

    def update(self, instance: Task, validated_data: dict):
        skip = validated_data.pop('skip', False)
        completed = validated_data.get('completed')
        repeat = validated_data.get('repeat')

        if skip:
            today = timezone.localdate()
            due_date = instance.due_date or today

            if due_date < today:
                days_overdue = (today - due_date).days
                intervals_to_add = -(-days_overdue // repeat)  # ceiling division
                due_date += timezone.timedelta(days=repeat * intervals_to_add)

            validated_data['due_date'] = due_date

        if completed and not instance.completed:
            CompletedTask.objects.create(task=instance)

        if not validated_data.get('due_date') and repeat:
                validated_data['due_date'] = timezone.now().date()

        if completed and repeat and not instance.completed:
            validated_data['due_date'] += timezone.timedelta(days=repeat)
            validated_data['completed'] = False

        return super().update(instance, validated_data)

    def create(self, validated_data:dict):
        repeat = validated_data.get('repeat')
        due_date = validated_data.get('due_date')

        if repeat and not due_date:
            validated_data['due_date'] = timezone.now().date()

        return super().create(validated_data)

class ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = List
        fields = ['id', 'title']

class TaskMinimalSerializer(serializers.ModelSerializer):
    list_title = serializers.SerializerMethodField('get_list_title')

    class Meta:
        model = Task
        fields = 'id', 'title', 'list_title', 'due_date'

    def get_list_title(self, task:Task) -> str | None:
        return task.list.title if task.list else None

class CompletedTaskSerializer(serializers.ModelSerializer):
    task = TaskMinimalSerializer()
    task_id = serializers.PrimaryKeyRelatedField(
        queryset=Task.objects.all(), source='task', write_only=True, required=False
        )

    class Meta:
        model = CompletedTask
        fields = 'id', 'completed_at', 'task', 'task_id'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        if request:
            self.fields['task_id'].queryset = Task.objects.filter(user=request.user)

        if self.instance:
            self.fields.pop('task_id', None)