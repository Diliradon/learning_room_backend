from django.urls import path, include
from rest_framework_nested import routers
from task_service.views import (
    TeachingTaskViewSet,
)
from course_service.urls import router

course_router = routers.NestedDefaultRouter(router, r"teaching-courses", lookup="course")
course_router.register("teaching-tasks", TeachingTaskViewSet, basename="teaching-tasks")

urlpatterns = [
    path("", include(course_router.urls))
]

app_name = "task-service"
