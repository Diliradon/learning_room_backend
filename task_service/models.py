from django.db import models

from learning_room_service.settings import AUTH_USER_MODEL


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
    type_of_task = models.CharField(choices=CHOICES_TYPE_OF_TASK, blank=False, )
    topic = models.CharField(max_length=150, null=False, blank=False)
    additionally = models.TextField(blank=True, null=False)
    answer_link = models.URLField(max_length=200, null=False, blank=True)
    answer_file = models.FileField(upload_to="uploads/", null=False, blank=True)
    answer_image = models.ImageField(upload_to="images/", null=False, blank=True)
    rating = models.CharField(choices=CHOICES_RATING, blank=False, null=False)
    for_whom = models.CharField(choices=CHOICES_FOR_WHOM, blank=False, null=False)
    students = models.ManyToManyField(
        AUTH_USER_MODEL,
        blank=True,
        null=False,
        related_name="doing_courses"
    )
