from django.urls import path, include
from rest_framework import routers

from course_service.views import (
    TeachingCourseViewSet,
)

router = routers.DefaultRouter()
router.register("teaching-courses", TeachingCourseViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "course_service"
