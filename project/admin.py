from django.contrib import admin
from leaflet.admin import LeafletGeoAdminMixin

from account.mixins import ExportCsvMixin, ExportXlsMixins
from project.models import Document, Project, ProjectSite

# Register your models here.

# admin.site.register(Project)
# admin.site.register(Document)


class ProjectSiteInline(LeafletGeoAdminMixin, admin.StackedInline):
    model = ProjectSite
    extra = 1


@admin.register(Project)
class ProjectAdmin(ExportCsvMixin, ExportXlsMixins, admin.ModelAdmin):
    list_display = [
        "title",
        "status",
        "created_at",
    ]
    actions = ["export_as_xls", "export_as_csv"]
    inlines = [ProjectSiteInline]


@admin.register(Document)
class DocumentAdmin(ExportCsvMixin, ExportXlsMixins, admin.ModelAdmin):
    list_display = ["name", "project"]
    actions = ["export_as_csv", "export_as_xls"]
