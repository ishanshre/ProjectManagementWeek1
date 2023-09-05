import uuid

from django.contrib.auth import get_user_model
from django.contrib.gis.db import models as geomodels
from django.contrib.gis.geos import LineString
from django.db import models
from django.utils.translation import gettext_lazy as _

from project.manager import DocumentManager, ProjectManager

User = get_user_model()


class Project(models.Model):
    ACTIVE = "Active"
    CANCELED = "Canceled"
    COMPLETED = "Completed"
    ON_HOLD = "On Hold"
    STATUS = [
        ("Active", _("Active")),
        ("Canceled", _("Canceled")),
        ("Completed", _("Completed")),
        ("On Hold", _("On Hold")),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=10000)
    status = models.CharField(max_length=10, choices=STATUS, default=ACTIVE)
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    active = ProjectManager()

    def __str__(self):
        return self.title


class Document(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="documents"
    )
    name = models.CharField(max_length=255)
    document = models.FileField(upload_to="project/files", null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="files"
    )
    objects = models.Manager()
    uploaded = DocumentManager()

    def __str__(self):
        return self.name


class ProjectSite(geomodels.Model):
    project = geomodels.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="sites"
    )
    site = geomodels.CharField(max_length=100)
    coordinate = geomodels.PointField(blank=True, null=True)
    area = geomodels.PolygonField(blank=True, null=True)
    way = geomodels.LineStringField(blank=True, null=True)
    created_at = geomodels.DateTimeField(auto_now_add=True)
    updated_at = geomodels.DateTimeField(auto_now=True)

    def __str__(self):
        return self.project.title

    def create_line_string(self):
        return LineString(self.coordinate, self.project.user.profile.home_address)

    def save(self, *args, **kwargs):
        if self.coordinate and self.project.user.profile.home_address:
            self.way = self.create_line_string()
        return super().save(*args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.coordinate and self.project.user.profile.home_address:
            self.way = self.create_line_string()
