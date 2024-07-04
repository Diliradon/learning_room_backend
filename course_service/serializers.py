from rest_framework import serializers
from course_service.models import Course


class TeachingCourseListSerializer(serializers.ModelSerializer):

    class Meta:
        models = Course
        fields = ("id", "name", "description", "unique_key")


class StudyingCourseListSerializer(serializers.ModelSerializer):

    class Meta:
        models = Course
        fields = ("id", "name", "description")

