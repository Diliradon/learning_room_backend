from django.db.models.signals import post_save
from django.dispatch import receiver
from course_service.models import Course


@receiver(post_save, sender=Course)
def add_creator_as_teacher(sender, instance, created, **kwargs):
    if created:
        instance.teachers.add(instance.creator)
