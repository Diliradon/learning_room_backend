import shortuuid
from django.db.models.signals import pre_save
from django.dispatch import receiver
from course_service.models import Course


@receiver(pre_save, sender=Course)
def add_unique_key(sender, instance, **kwargs):
    if not instance.unique_key:
        instance.unique_key = shortuuid.ShortUUID.random(length=6)
