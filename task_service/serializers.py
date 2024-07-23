from rest_framework import serializers
from task_service.models import (
    Task,
)


class TeachingTaskCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "topic",
            "type_of_task",
            "additionally",
            "task_link",
            "rating",
            "for_whom",
            "deadline",
            "students",
        )


class TeachingTaskDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = (
            "id",
            "topic",
            "type_of_task",
            "additionally",
            "task_link",
            "rating",
            "for_whom",
            "deadline",
            "students",
        )


class TeachingTaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "topic", "rating", "deadline")
