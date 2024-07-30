from rest_framework import viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from course_service.serializers import UserByDetailTeachingSerializer

from course_service.models import Course
from task_service.models import Task, Answer

from task_service.serializers import (
    TaskListSerializer,
    TeachingTaskCreateUpdateSerializer,
    TeachingTaskDetailSerializer,
    StudyingTaskDetailSerializer,
    AnswerCreateUpdateSerializer, AnswerSerializer,
)


class TeachingTaskViewSet(viewsets.ModelViewSet):

    def get_serializer_class(self):

        if self.action == "list":
            return TaskListSerializer

        if self.action == "retrieve":
            return TeachingTaskDetailSerializer

        if self.action in ["create", "update", "partial_update"]:
            return TeachingTaskCreateUpdateSerializer

        return TaskListSerializer

    def get_queryset(self):
        queryset = Task.objects.all()
        course_id = self.kwargs.get('course_pk')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        course_id = self.kwargs.get("course_pk")
        serializer.save(course_id=course_id)


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


class StudyingTaskViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Task.objects.select_related("course").prefetch_related("students")

    def get_serializer_class(self):

        if self.action == "retrieve":
            return StudyingTaskDetailSerializer

        return TaskListSerializer

    def get_queryset(self):
        queryset = self.queryset
        course_id = self.kwargs.get('course_pk')
        queryset = queryset.filter(course_id=course_id, students=self.request.user)

        return queryset


class StudyingAnswerViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(student=user)

    def get_serializer_class(self):

        if self.action in ("create", "update",):
            return AnswerCreateUpdateSerializer

        return AnswerSerializer

    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_pk")
        user_pk = self.request.user.pk
        serializer.save(task_id=task_id, student_id=user_pk)
