from datetime import datetime

from django.db.models import Q
from django_filters import filters
from django_filters import rest_framework as drf_filters

from account.models import User


class UserStatFilter(drf_filters.FilterSet):
    project_created_at = drf_filters.DateFilter(
        label="Project Created Date At",
        field_name="projects__created_at__date",
    )
    project_created_month = drf_filters.NumberFilter(
        label="Project Created Filter at Month",
        field_name="projects__created_at__month",
    )
    files_uploaded_at = drf_filters.DateFilter(
        label="Files Uploaded Date At",
        field_name="files__uploaded_at__date",
    )
    files_uploaded_month = drf_filters.NumberFilter(
        label="Files Uploaded Month",
        field_name="files__uploaded_at__month",
    )

    class Meta:
        model = User
        fields = []

    def filter_queryset(self, queryset):
        params = self.data
        print(params)
        q_obj = Q()
        project_created = "project_created_at"
        if project_created in params and params[project_created]:
            q_obj = Q(projects__created_at__date=params[project_created])
            queryset = queryset.filter(q_obj)
        if "project_created_month" in params and params["project_created_month"]:
            q_obj = Q(projects__created_at__month=params["project_created_month"])
            queryset = queryset.filter(q_obj)
        if "files_uploaded_at" in params and params["files_uploaded_at"]:
            q_obj = Q(files__uploaded_at__date=params["files_uploaded_at"])
            queryset = queryset.filter(q_obj)
        if "files_uploaded_month" in params and params["files_uploaded_month"]:
            q_obj = Q(files__uploaded_at__month=params["files_uploaded_month"])
            queryset = queryset.filter(q_obj)
        return super().filter_queryset(queryset)
