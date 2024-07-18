from rest_framework import viewsets, mixins


class TeachingTaskViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
):
    pass
