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


class StudyingCourseListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "description")
