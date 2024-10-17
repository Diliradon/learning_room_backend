from django.contrib.auth import get_user_model
from rest_framework import serializers
from course_service.models import Course, LENGTH_UNIQUE_KEY
from task_service.models import Task
from task_service.serializers import TaskListSerializer


class UserByDetailTeachingSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name")


class TeachingCourseListSerializer(serializers.ModelSerializer):
    teachers = UserByDetailTeachingSerializer(many=True, read_only=False)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "color",
            "unique_key",
            "created_date",
            "teachers",
        )


class TeachingCourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "unique_key",
            "teachers",
            "students",
            "number_of_classroom",
        )


class TeachingCourseDetailSerializer(serializers.ModelSerializer):
    students = UserByDetailTeachingSerializer(many=True, read_only=True)
    teachers = UserByDetailTeachingSerializer(many=True, read_only=True)
    tasks = TaskListSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "unique_key",
            "color",
            "number_of_classroom",
            "created_date",
            "teachers",
            "students",
            "tasks",
        )


class TeachingCourseUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "unique_key",
            "color",
            "number_of_classroom",
            "created_date",
        )

    def update(self, instance, validated_data):

        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.unique_key = validated_data.get("unique_key", instance.unique_key)
        instance.color = validated_data.get("color", instance.color)
        instance.number_of_classroom = validated_data.get("number_of_classroom", instance.number_of_classroom)
        instance.save()

        return instance


class StudyingCourseListSerializer(serializers.ModelSerializer):
    teachers = UserByDetailTeachingSerializer(many=True, read_only=False)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "number_of_classroom", "teachers")


class JoinToCourseByKeySerializer(serializers.Serializer):
    unique_key = serializers.CharField(required=True)

    def validate_unique_key(self, value):

        if len(value) != LENGTH_UNIQUE_KEY:
            raise serializers.ValidationError(
                f"Unique key must be {LENGTH_UNIQUE_KEY} characters long!"
            )

        return value


class StudyingCourseDetailSerializer(serializers.ModelSerializer):
    students = UserByDetailTeachingSerializer(many=True, read_only=True)
    teachers = UserByDetailTeachingSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "number_of_classroom",
            "created_date",
            "teachers",
            "students",
            "tasks",
        )
