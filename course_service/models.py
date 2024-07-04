from django.db import models
import shortuuid
from learning_room_service.settings import AUTH_USER_MODEL


class Task(models.Model):
    pass


class Course(models.Model):
    name = models.CharField(null=False, blank=False, max_length=100)
    description = models.TextField(null=False, blank=True)
    unique_key = models.CharField(default=shortuuid.uuid, max_length=22, unique=True)
    creator = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    teachers = models.ManyToManyField(AUTH_USER_MODEL)
    students = models.ManyToManyField(AUTH_USER_MODEL, blank=True)
    tasks = models.ManyToManyField(Task, blank=True)

    class Meta:
        unique_together = ["teachers", "students"]
        ordering = ["name"]

    def __str__(self):
        return self.name
