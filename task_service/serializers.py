from rest_framework import serializers
from task_service.models import (
    Task,
    AnswerImage,
    AnswerFile,
    TaskFile,
    TaskImage,
)


class AnswerImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerImage
        fields = ("id", "image")


class TaskImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskImage
        fields = ("id", "image")


class AnswerFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AnswerFile
        fields = ("id", "file")


class TaskFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = TaskFile
        fields = ("id", "file")


class TeachingTaskCreateSerializer(serializers.ModelSerializer):
    task_files = TaskFileSerializer(many=True, write_only=True)
    task_images = TaskImageSerializer(many=True, write_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "topic",
            "type_of_task",
            "additionally",
            "task_link",
            "task_images",
            "task_files",
            "rating",
            "for_whom",
            "deadline",
            "students",
        )


class TeachingTaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "topic", "rating", "deadline")
