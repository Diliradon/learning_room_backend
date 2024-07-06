from django.urls import path, include
from rest_framework import routers

from course_service.views import (
    TeachingCourseViewSet,
    StudyingCourseViewSet,
)

router = routers.DefaultRouter()
router.register("teaching-courses", TeachingCourseViewSet, basename="teaching-courses")
router.register("studying-courses", StudyingCourseViewSet, basename="studying-courses")

urlpatterns = [path("", include(router.urls))]

app_name = "course_service"
