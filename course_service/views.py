from rest_framework import viewsets
from course_service.serializers import (
    TeachingCourseListSerializer,
)
from course_service.models import Course


class TeachingCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        if self.action == "list":
            return TeachingCourseListSerializer

        return TeachingCourseListSerializer

    def get_queryset(self):
        user = self.request.user
        return user.teaching_courses.all()
