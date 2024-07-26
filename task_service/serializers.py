from rest_framework import serializers
from task_service.models import (
    Task,
    LearningFile,
    Answer
)


class LearningFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = LearningFile
        fields = ('id', 'file_url', 'type')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.file.url)
        return obj.file.url


class TeachingTaskCreateUpdateSerializer(serializers.ModelSerializer):
    task_file = serializers.FileField(
        max_length=100000,
        allow_empty_file=False,
        use_url=False,
        write_only=True,
        required=False
    )
    task_image = serializers.ImageField(
        max_length=100000,
        allow_empty_file=False,
        use_url=False,
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
            "task_image",
            "task_file",
            "rating",
            "for_whom",
            "deadline",
            "students",
        )

    def create(self, validated_data):
        file_data = validated_data.pop('task_file', None)
        image_data = validated_data.pop('task_image', None)
        students_data = validated_data.pop('students', [])

        task = Task.objects.create(**validated_data)
        task.students.set(students_data)

        if file_data:
            LearningFile.objects.create(
                model="Task",
                type="file",
                instance_id=task.pk,
                file=file_data
            )
        if image_data:
            LearningFile.objects.create(
                model="Task",
                type="image",
                instance_id=task.pk,
                file=image_data
            )
        return task

    def update(self, instance, validated_data):
        file_data = validated_data.pop('task_file', None)
        image_data = validated_data.pop('task_image', None)
        students_data = validated_data.pop('students', [])

        instance = super().update(instance, validated_data)
        instance.students.set(students_data)

        if file_data:
            LearningFile.objects.create(
                model="Task",
                type="file",
                instance_id=instance.pk,
                file=file_data
            )
        if image_data:
            LearningFile.objects.create(
                model="Task",
                type="image",
                instance_id=instance.pk,
                file=image_data
            )
        return instance


class TeachingTaskDetailSerializer(serializers.ModelSerializer):
    task_files = serializers.SerializerMethodField()
    task_images = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = (
            "id",
            "topic",
            "type_of_task",
            "additionally",
            "task_link",
            "task_files",
            "task_images",
            "rating",
            "for_whom",
            "deadline",
            "students",
        )

    def get_task_files(self, obj):
        files = obj.task_files
        serializer = LearningFileSerializer(files, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_task_images(self, obj):
        images = obj.task_images
        serializer = LearningFileSerializer(images, many=True, context={'request': self.context.get('request')})
        return serializer.data


class StudyingTaskDetailSerializer(TeachingTaskDetailSerializer):

    class Meta(TeachingTaskDetailSerializer.Meta):
        fields = (
            "id",
            "topic",
            "type_of_task",
            "additionally",
            "task_link",
            "task_files",
            "task_images",
            "rating",
            "deadline",
        )


class TaskListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = ("id", "topic", "rating", "deadline")


class AnswerCreateUpdateSerializer(serializers.ModelSerializer):
    answer_file = serializers.FileField(
        max_length=100000,
        allow_empty_file=False,
        use_url=False,
        write_only=True,
        required=False
    )
    answer_image = serializers.ImageField(
        max_length=100000,
        allow_empty_file=False,
        use_url=False,
        write_only=True,
        required=False
    )

    class Meta:
        model = Answer
        fields = ("id", "description", "answer_file", "answer_image", "answer_link")

    def create(self, validated_data):
        file_data = validated_data.pop("answer_file", None)
        image_data = validated_data.pop("answer_image", None)

        answer = Answer.objects.create(**validated_data)

        if file_data:
            LearningFile.objects.create(
                model="Answer",
                type="file",
                instance_id=answer.pk,
                file=file_data
            )
        if image_data:
            LearningFile.objects.create(
                model="Answer",
                type="image",
                instance_id=answer.pk,
                file=image_data
            )
        return answer

    def update(self, instance, validated_data):
        file_data = validated_data.pop("task_file", None)
        image_data = validated_data.pop("task_image", None)

        instance = super().update(instance, validated_data)

        if file_data:
            LearningFile.objects.create(
                model="Answer",
                type="file",
                instance_id=instance.pk,
                file=file_data
            )
        if image_data:
            LearningFile.objects.create(
                model="Answer",
                type="image",
                instance_id=instance.pk,
                file=image_data
            )
        return instance


class AnswerSerializer(serializers.ModelSerializer):
    task = TaskListSerializer(many=False, read_only=True)
    answer_files = serializers.SerializerMethodField()
    answer_images = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = (
            "id",
            "task",
            "description",
            "answer_images",
            "answer_files",
            "answer_link",
            "status",
        )

    def get_answer_files(self, obj):
        files = obj.answer_files
        serializer = LearningFileSerializer(files, many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_answer_images(self, obj):
        images = obj.answer_images
        serializer = LearningFileSerializer(images, many=True, context={'request': self.context.get('request')})
        return serializer.data
