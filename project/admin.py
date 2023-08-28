from django.contrib import admin

from project.models import Document, Project

# Register your models here.

admin.site.register(Project)
admin.site.register(Document)
