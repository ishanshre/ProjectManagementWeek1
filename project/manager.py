from django.db import models
from django.db.models.query import QuerySet


class ProjectManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().filter(status="Active")


class DocumentManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset().order_by("-uploaded_at")
