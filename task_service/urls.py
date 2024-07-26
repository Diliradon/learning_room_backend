from django.urls import path, include
from rest_framework_nested import routers
from task_service.views import (
    TeachingTaskViewSet,
    get_course_students,
    StudyingTaskViewSet,
    StudyingAnswerViewSet,
)
from course_service.urls import router

teaching_course_router = routers.NestedDefaultRouter(
    router,
    r"teaching-courses",
    lookup="course",
)
teaching_course_router.register(
    "teaching-tasks",
    TeachingTaskViewSet,
    basename="teaching-tasks",
)
studying_course_router = routers.NestedDefaultRouter(
    router,
    r"studying-courses",
    lookup="course",
)

studying_course_router.register(
    "studying-tasks",
    StudyingTaskViewSet,
    basename="studying-tasks",
)

studying_task_router = routers.NestedDefaultRouter(
    studying_course_router,
    "studying-tasks",
    lookup="task",
)
studying_task_router.register(
    "studying-answer",
    StudyingAnswerViewSet,
    basename="studying-answer",
)

urlpatterns = [
    path("", include(teaching_course_router.urls)),
    path("", include(studying_course_router.urls)),
    path("", include(studying_task_router.urls)),
    path(
        "teaching-courses/<int:course_pk>/students/",
        get_course_students,
        name="course-students"
    ),
]

app_name = "task-service"
