from rest_framework import viewsets

from task_service.models import Task

from task_service.serializers import (
    TeachingTaskListSerializer,
    TaskSerializer,
)


class TeachingTaskViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):

        if self.action == "list":
            return TeachingTaskListSerializer

        return TaskSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        course_id = self.kwargs.get('course_pk')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        course_id = self.kwargs.get('course_pk')
        serializer.save(course_id=course_id)
