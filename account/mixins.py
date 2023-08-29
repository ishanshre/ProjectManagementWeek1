"""
Custom mixins
"""
import csv

import xlsxwriter
from django.http import HttpResponse
from django.utils import timezone


class ExportCsvMixin:
    """
    This class deals with the csv exports action for admin
    """

    def export_as_csv(self, request, queryset):
        # get the model from query set
        model = queryset.model
        # get the metadata of the models
        meta = model._meta
        # get a list of concrete fields
        field_names = [field.name for field in meta.concrete_fields]
        # create a csv response with headers
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={meta}.csv"},
        )
        # create a csv
        writer = csv.writer(response)
        # write the table head of the csv
        writer.writerow(field_names)
        for obj in queryset:
            # write the records of the csv
            writer.writerow([getattr(obj, field) for field in field_names])
        return response

    export_as_csv.short_description = "Export selected as CSV"

    def export_profile_as_csv(self, request, queryset):
        """
        This method is only for user with profile having one to one relationship
        """
        model = queryset.model
        # get the profile field
        profile_field = model._meta.get_field("profile")
        # get the profile model using one to one reverse relationship
        profile_model = profile_field.related_model
        # get the profile meta
        meta = profile_model._meta
        # get the profile model fields
        field_names = [field.name for field in meta.concrete_fields]
        response = HttpResponse(
            content_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={meta}.csv",
            },
        )

        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            profile = getattr(obj, "profile", None)
            if profile:
                writer.writerow([getattr(profile, field) for field in field_names])
        return response

    export_profile_as_csv.short_description = "Export profile as csv"


class ExportXlsMixins:
    def export_as_xls(self, request, queryset):
        model = queryset.model
        meta = model._meta
        field_names = [field.name for field in meta.concrete_fields]
        response = HttpResponse(
            content_type="text/xls",
            headers={"Content-Disposition": f"attachment; filename={meta}.xls"},
        )
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        for field_name in field_names:
            worksheet.write(row, col, field_name)
            col += 1

        for obj in queryset:
            row += 1
            col = 0
            for field_name in field_names:
                value = getattr(obj, field_name)

                if isinstance(value, timezone.datetime):
                    value = value.astimezone(timezone.utc).replace(tzinfo=None)

                if isinstance(value, object):
                    value = value.__str__()
                worksheet.write(row, col, value)

                col += 1
        workbook.close()
        return response

    export_as_xls.short_description = "Export selected as XLS"

    def export_profile_as_xls(self, request, queryset):
        model = queryset.model
        # get the profile field
        profile_field = model._meta.get_field("profile")
        # get the profile mode using reverse relationship
        profile_model = profile_field.related_model
        # get profile meta
        meta = profile_model._meta
        # get the field names
        field_names = [field.name for field in meta.concrete_fields]
        response = HttpResponse(
            content_type="text/xls",
            headers={
                "Content-Disposition": f"attachment; filename={meta}.xls",
            },
        )
        workbook = xlsxwriter.Workbook(response)
        worksheet = workbook.add_worksheet()
        row = 0
        col = 0

        for field_name in field_names:
            worksheet.write(row, col, field_name)
            col += 1

        for obj in queryset:
            profile = getattr(obj, "profile", None)
            if profile:
                row += 1
                col = 0
                for field_name in field_names:
                    value = getattr(profile, field_name)
                    if isinstance(value, timezone.datetime):
                        value = value.astimezone(timezone.utc).replace(tzinfo=None)
                    if isinstance(value, object):
                        value = value.__str__()
                    worksheet.write(row, col, value)
                    col += 1
        workbook.close()
        return response

    export_profile_as_xls.short_description = "Export Profile as xls"
