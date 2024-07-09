from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from course_service.serializers import (
    TeachingCourseListSerializer,
    TeachingCourseCreateSerializer,
    TeachingCourseDetailSerializer,
    StudyingCourseListSerializer,
    JoinToCourseByKeySerializer,
    StudyingCourseDetailSerializer,
)
from course_service.models import Course


class TeachingCourseViewSet(
    viewsets.ModelViewSet
):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        if self.action == "create":
            return TeachingCourseCreateSerializer

        if self.action == "retrieve" or self.action == "update":
            return TeachingCourseDetailSerializer

        return TeachingCourseListSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")

        if name:
            self.queryset.filter(name=name)

        user = self.request.user
        return user.teaching_courses.prefetch_related("students", "teachers", "tasks")

    def perform_create(self, serializer):
        course = serializer.save(creator=self.request.user)
        course.teachers.add(self.request.user)

        if course.students.filter(id=self.request.user.id).exists():
            course.students.remove(self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()

        if course.students.filter(id=self.request.user.id).exists():
            course.students.remove(self.request.user)


class StudyingCourseViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
):
    queryset = Course.objects.all()

    def get_serializer_class(self):

        if self.action == 'join_the_course_by_unique_key':
            return JoinToCourseByKeySerializer

        if self.action == "retrieve":
            return StudyingCourseDetailSerializer

        return StudyingCourseListSerializer

    def get_queryset(self):
        name = self.request.query_params.get("name")

        if name:
            self.queryset.filter(name=name)

        user = self.request.user
        return user.studying_courses.prefetch_related("students", "teachers", "tasks")

    @action(
        methods=["POST"],
        detail=False,
        url_path="join-course"
    )
    def join_the_course_by_unique_key(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        unique_key = serializer.validated_data["unique_key"]

        try:
            course = Course.objects.get(unique_key=unique_key)

        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if course.teachers.filter(id=request.user.id).exists():
            return Response({"detail": "You are a teacher in this course!"}, status=status.HTTP_409_CONFLICT)

        if course.students.filter(id=request.user.id).exists():
            return Response({"detail": "You are already connected to the course!"}, status=status.HTTP_409_CONFLICT)

        course.students.add(user)
        course.save()

        return Response({"detail": "Successfully joined the course."}, status=status.HTTP_200_OK)
