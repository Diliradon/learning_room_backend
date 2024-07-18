from rest_framework import viewsets, mixins

from task_service.models import Task

from task_service.serializers import (
    TeachingTaskListSerializer,
)


class TeachingTaskViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    queryset = Task.objects.all()

    def get_serializer_class(self):

        if self.action == "list":
            return TeachingTaskListSerializer

        return TeachingTaskListSerializer
