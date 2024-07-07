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
    students = UserByDetailTeachingSerializer(many=True, read_only=False)
    teachers = UserByDetailTeachingSerializer(many=True, read_only=False)

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


class JoinToCourseByKeySerializer(serializers.Serializer):
    unique_key = serializers.CharField(required=True)

    def validate_unique_key(self, value):

        if len(value) != 22:
            raise serializers.ValidationError("Unique key must be 22 characters long!")

        return value


class StudyingCourseDetailSerializer(serializers.ModelSerializer):
    students = UserByDetailTeachingSerializer(many=True, read_only=True)
    teachers = UserByDetailTeachingSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ("id", "name", "description", "teachers", "students", "tasks")
