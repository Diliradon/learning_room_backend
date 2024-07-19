from rest_framework import serializers
from task_service.models import Task


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = "__all__"


class TeachingTaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "topic", "rating", "deadline")
