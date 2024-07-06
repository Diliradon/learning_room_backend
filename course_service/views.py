from rest_framework import viewsets, mixins
from course_service.serializers import (
    TeachingCourseListSerializer,
    TeachingCourseCreateSerializer,
    TeachingCourseDetailSerializer,
    StudyingCourseListSerializer,
)
from course_service.models import Course


class TeachingCourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        if self.action == "create":
            return TeachingCourseCreateSerializer

        if self.action == "retrieve":
            return TeachingCourseDetailSerializer

        return TeachingCourseListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.teaching_courses.prefetch_related("students", "teachers", "tasks")

    def perform_create(self, serializer):
        course = serializer.save(creator=self.request.user)
        course.teachers.add(self.request.user)


class StudyingCourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        return StudyingCourseListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.studying_courses.prefetch_related("students", "teachers", "tasks")
