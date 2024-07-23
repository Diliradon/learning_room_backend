import os
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from learning_room_service.settings import AUTH_USER_MODEL
from course_service.models import Course


def media_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.task.topic)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/", filename)


class LearningFile(models.Model):
    CHOICES_MODEL = (
        ("Task", "Task"),
        ("Answer", "Answer"),
    )
    CHOICES_TYPE = (
        ("file", "file"),
        ("image", "image"),
    )
    model = models.CharField(max_length=30, choices=CHOICES_MODEL)
    type = models.CharField(max_length=30, choices=CHOICES_TYPE)
    instance_id = models.IntegerField()
    file = models.FileField(upload_to=media_path)


class Task(models.Model):
    CHOICES_TYPE_OF_TASK = (
        (1, "Theoretical task"),
        (2, "Practical task"),
        (3, "Control task"),
        (4, "Another task"),
    )
    CHOICES_RATING = (
        (1, "No rating!"),
        (5, "5-points"),
        (12, "12-points"),
        (100, "100-points"),
    )
    CHOICES_FOR_WHOM = (
        (1, "All students"),
        (2, "Select students"),
    )
    type_of_task = models.IntegerField(choices=CHOICES_TYPE_OF_TASK, blank=False, null=False)
    topic = models.CharField(max_length=150, null=False, blank=False)
    additionally = models.TextField(blank=True, null=False)
    task_link = models.URLField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(choices=CHOICES_RATING, blank=False, null=False)
    for_whom = models.IntegerField(choices=CHOICES_FOR_WHOM, blank=False, null=False)
    students = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name="doing_courses"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks")
    deadline = models.DateTimeField(null=True, blank=True)

    @property
    def task_files(self):
        return LearningFile.objects.filter(type="file", model="Task", instance_id=self.pk)

    @property
    def task_imges(self):
        return LearningFile.objects.filter(type="image", model="Task", instance_id=self.pk)

    def clean(self):
        if self.for_whom == 1 and self.students.exists():
            raise ValidationError("You cannot select students when 'for_whom' is set to 'All students'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic


class Answer(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    student = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    answer_link = models.URLField(max_length=200, null=True, blank=True)
    description = models.TextField(blank=True, null=True)


class Review(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name="reviews")
    note = models.IntegerField()
    rationale = models.CharField(max_length=200, blank=True, null=True)
