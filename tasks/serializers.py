from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Task, List, CompletedTask
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = 'id', 'title', 'description', 'created_at', 'completed', 'repeat', 'due_date', 'list'

    def get_fields(self):
        fields = super().get_fields()
        if self.context.get('request').method == 'POST':
            fields.pop('completed', None)
            fields.pop('list', None)
        
        elif self.context.get('request').method in ('PUT', 'PATCH'):
            fields.pop('user', None)

        return fields

    def update(self, instance: Task, validated_data: dict):
        completed = validated_data.get('completed')
        repeat = validated_data.get('repeat')

        if not validated_data.get('due_date') and repeat:
                validated_data['due_date'] = timezone.now().date()

        if completed and repeat and not instance.completed:
            CompletedTask.save(instance)
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