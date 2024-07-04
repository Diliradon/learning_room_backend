from rest_framework import viewsets
from course_service.serializers import (
    TeachingCourseListSerializer,
)


class TeachingCourseViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):
        if self.action == "list":
            return TeachingCourseListSerializer
