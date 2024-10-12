from django.db import models
from learning_room_service.settings import AUTH_USER_MODEL

LENGTH_UNIQUE_KEY = 6


class Course(models.Model):
    COLOR_CHOICES = (
        ("secondary-400", "#A6DCEF"),
        ("secondary-100", "#77D99F"),
        ("secondary-200", "#FDB7AA"),
        ("primary-100", "#D2ADE6"),
        ("secondary-300", "#F9E783"),
    )

    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=False, blank=True)
    unique_key = models.CharField(
        max_length=LENGTH_UNIQUE_KEY,
        unique=True,
        blank=True
    )
    color = models.CharField(null=False, blank=False, default="secondary-400")
    created_date = models.DateField(auto_now=True)
    number_of_classroom = models.CharField(default="Online only!")
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_courses"
    )
    teachers = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name="teaching_courses",
    )
    students = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name="studying_courses"
    )

    class Meta:
        ordering = ["-created_date", "name"]

    def __str__(self):
        return self.name
