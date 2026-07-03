from rest_framework import serializers
from .models import Task, List, CompletedTask
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    list_title = serializers.SerializerMethodField('get_list_title')

    class Meta:
        model = Task
        fields = 'id', 'title', 'description', 'created_at', 'completed', 'repeat', 'due_date', 'list_title'

    def get_list_title(self, task:Task) -> str:
        return task.list.title if task.list else None

    def get_fields(self) -> dict[str, Task]:
        fields = super().get_fields()
        request = self.context.get('request')

        if not request:
            return fields

        if request.method == 'POST':
            fields.pop('completed', None)
        
        elif request.method in ('PUT', 'PATCH'):
            fields.pop('user', None)

        return fields

    def update(self, instance: Task, validated_data: dict):
        completed = validated_data.get('completed')
        repeat = validated_data.get('repeat')

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