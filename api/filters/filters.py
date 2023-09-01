import django_filters
from django.db.models import Q
from django_filters import rest_framework as drf_filter

from account.models import Department
from project.models import Document


class DocumentFilter(drf_filter.FilterSet):
    department = drf_filter.CharFilter(label="Department Name Contains")

    class Meta:
        model = Document
        fields = {
            "name": ["icontains"],
            "uploaded_at": [
                "year",
                "date",
                "date__range",
            ],
        }

    def filter_queryset(self, queryset):
        params = self.data
        q_obj = Q()
        if "department" in params and params["department"]:
            q_obj = Q(uploaded_by__department__name__icontains=params["department"])
            queryset = queryset.filter(q_obj)
        return super().filter_queryset(queryset)
