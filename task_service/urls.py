from django.urls import path, include
from rest_framework import routers
from task_service.views import (
    TeachingTaskViewSet,
)

router = routers.DefaultRouter()
router.register("teaching-tasks", TeachingTaskViewSet, basename="teaching-tasks")

urlpatterns = [
    path("", include(router.urls))
]


app_name = "task-service"
