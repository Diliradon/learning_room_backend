import shortuuid
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from course_service.models import Course


@receiver(post_save, sender=Course)
def add_creator_as_teacher(sender, instance, created, **kwargs):
    if created:
        instance.teachers.add(instance.creator)


@receiver(pre_save, sender=Course)
def add_unique_key(sender, instance, **kwargs):
    if not instance.unique_key:
        instance.unique_key = shortuuid.uuid()
