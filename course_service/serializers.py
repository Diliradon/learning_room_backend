from django.contrib.auth import get_user_model
from rest_framework import serializers
from course_service.models import Course


class TeachingCourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "description", "unique_key")


class TeachingCourseCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "description", "unique_key", "teachers", "students")


class UserByDetailTeachingSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name")


class TeachingCourseDetailSerializer(serializers.ModelSerializer):
    students = UserByDetailTeachingSerializer(many=True, read_only=True)
    teachers = UserByDetailTeachingSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = (
            "id",
            "name",
            "description",
            "unique_key",
            "teachers",
            "students",
            "tasks"
        )


class StudyingCourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "description")



