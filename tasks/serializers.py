from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get('request')

        if request and request.method in ('PUT', 'PATCH'):
            self.fields['completed'].read_only = False
        else:
            self.fields['completed'].read_only = True
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'completed', 'repeat', 'description', 'created_at', 'user', 'due_date'
            ]
        read_only_fields = ['user']