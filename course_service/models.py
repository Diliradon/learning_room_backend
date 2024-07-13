from django.db import models
from learning_room_service.settings import AUTH_USER_MODEL


class Task(models.Model):
    pass


class Course(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=False, blank=True)
    unique_key = models.CharField(max_length=6, unique=True, blank=False, null=False)
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
    tasks = models.ManyToManyField(Task, blank=True)

    class Meta:
        ordering = ["-created_date", "name"]

    def __str__(self):
        return self.name
