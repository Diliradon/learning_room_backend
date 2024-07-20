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


class TeachingTaskCreateUpdateSerializer(serializers.ModelSerializer):
    task_files = serializers.ListField(
        child=serializers.FileField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    task_images = serializers.ListField(
        child=serializers.ImageField(max_length=100000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )

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

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        images_data = validated_data.pop('images', [])
        students_data = validated_data.pop('students', [])

        task = Task.objects.create(**validated_data)

        task.students.set(students_data)

        for file_data in files_data:
            TaskFile.objects.create(task=task, file=file_data)
        for image_data in images_data:
            TaskImage.objects.create(task=task, image=image_data)
        return task

    def update(self, instance, validated_data):
        files_data = validated_data.pop('files', [])
        images_data = validated_data.pop('images', [])
        students_data = validated_data.pop('students', [])

        instance = super().update(instance, validated_data)

        instance.students.set(students_data)
        for file_data in files_data:
            TaskFile.objects.create(task=instance, file=file_data)
        for image_data in images_data:
            TaskImage.objects.create(task=instance, image=image_data)
        return instance


class TeachingTaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "topic", "rating", "deadline")
