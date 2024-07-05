from rest_framework import viewsets, mixins
from course_service.serializers import (
    TeachingCourseListSerializer,
    TeachingCourseCreateSerializer,
)
from course_service.models import Course


class TeachingCourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        if self.action == "create":
            return TeachingCourseCreateSerializer

        return TeachingCourseListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.teaching_courses.all()

    def perform_create(self, serializer):
        course = serializer.save(creator=self.request.user)
        course.teachers.add(self.request.user)
