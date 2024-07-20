from django.core.exceptions import ValidationError
from django.db import models
from learning_room_service.settings import AUTH_USER_MODEL
from course_service.models import Course
from user.models import  movie_image_file_path


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
    answer_link = models.URLField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(choices=CHOICES_RATING, blank=False, null=False)
    note = models.IntegerField(null=True, blank=True)
    for_whom = models.IntegerField(choices=CHOICES_FOR_WHOM, blank=False, null=False)
    students = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        related_name="doing_courses"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="tasks")
    deadline = models.DateTimeField(null=True, blank=True)

    def clean(self):
        if self.for_whom == 1 and self.students.exists():
            raise ValidationError("You cannot select students when 'for_whom' is set to 'All students'.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.topic


class TaskFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_files")
    file = models.FileField(upload_to=movie_image_file_path)


class TaskImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task_images")
    image = models.ImageField(upload_to=movie_image_file_path)


class AnswerFile(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="answer_files")
    file = models.FileField(upload_to=movie_image_file_path)


class AnswerImage(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="answer_images")
    image = models.ImageField(upload_to=movie_image_file_path)
