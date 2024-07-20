from django.urls import path, include
from rest_framework_nested import routers
from task_service.views import (
    TeachingTaskViewSet,
    get_course_students,
)
from course_service.urls import router

course_router = routers.NestedDefaultRouter(router, r"teaching-courses", lookup="course")
course_router.register("teaching-tasks", TeachingTaskViewSet, basename="teaching-tasks")

urlpatterns = [
    path("", include(course_router.urls)),
    path(
        "teaching-courses/<int:course_pk>/students/",
        get_course_students,
        name="course-students"
    ),
]

app_name = "task-service"
