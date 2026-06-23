from rest_framework import serializers
from .models import Task, List
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
            fields.pop('completed', None)
            fields.pop('user', None)
            fields.pop('list', None)

        return fields

    def validate(self, attrs):
        attrs['user'] = self.context('request').user

        attrs['list'] = List.objects.filter(pk=self.context.get('list_pk'), user=attrs['user']).first()

        if attrs['list']:
            raise 

        return super().validate(attrs)

    def update(self, instance: Task, validated_data: dict):
        completed = validated_data.get('completed')
        repeat = validated_data.get('repeat')

        if completed and repeat:
            if not validated_data.get('due_date'):
                validated_data['due_date'] = timezone.now().date()
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