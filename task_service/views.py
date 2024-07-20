from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from course_service.serializers import UserByDetailTeachingSerializer

from course_service.models import Course
from task_service.models import Task, TaskImage, TaskFile

from task_service.serializers import (
    TeachingTaskListSerializer,
    TeachingTaskCreateUpdateSerializer,
    TeachingTaskDetailSerializer,
)


class TeachingTaskViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):

        if self.action == "list":
            return TeachingTaskListSerializer

        if self.action == "retrieve":
            return TeachingTaskDetailSerializer

        if self.action in ["create", "update", "partial_update"]:
            return TeachingTaskCreateUpdateSerializer

        return TeachingTaskListSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        course_id = self.kwargs.get('course_pk')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_pk")
        task = serializer.save(course_id=course_id)

        files = self.request.FILES.getlist("task_files")
        for file in files:
            TaskFile.objects.create(task=task, file=file)

        images = self.request.FILES.getlist("task_images")
        for image in images:
            TaskImage.objects.create(task=task, image=image)

    def perform_update(self, serializer):
        task = serializer.save()

        files = self.request.FILES.getlist("task_files")
        for file in files:
            TaskFile.objects.create(task=task, file=file)

        images = self.request.FILES.getlist("task_images")
        for image in images:
            TaskImage.objects.create(task=task, image=image)


@api_view(["GET"])
def get_course_students(request, course_pk):
    try:
        course = Course.objects.get(pk=course_pk)
    except Course.DoesNotExist:
        return Response(
            {"detail": "Course not found."},
            status=status.HTTP_404_NOT_FOUND
        )

    students = course.students.all()
    serializer = UserByDetailTeachingSerializer(students, many=True)
    return Response(serializer.data)
