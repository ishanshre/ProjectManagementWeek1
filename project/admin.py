from django.contrib import admin

from account.mixins import ExportCsvMixin, ExportXlsMixins
from project.models import Document, Project

# Register your models here.

# admin.site.register(Project)
# admin.site.register(Document)


@admin.register(Project)
class ProjectAdmin(ExportCsvMixin, ExportXlsMixins, admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "created_at",
    ]
    actions = ["export_as_xls", "export_as_csv"]


@admin.register(Document)
class DocumentAdmin(ExportCsvMixin, ExportXlsMixins, admin.ModelAdmin):
    list_display = ["name", "project"]
    actions = ["export_as_csv", "export_as_xls"]
