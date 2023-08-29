from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.forms import CustomUserChangeForm, CustomUserCreationForm
from account.mixins import ExportCsvMixin, ExportXlsMixins
from account.models import Department, Profile

User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile


@admin.register(User)
class UserAdmin(ExportCsvMixin, ExportXlsMixins, BaseUserAdmin):
    list_display = ["username", "department", "is_staff"]
    actions = [
        "export_as_csv",
        "export_as_xls",
        "export_profile_as_csv",
        "export_profile_as_xls",
    ]
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "None",
            {
                "fields": ("department",),
            },
        ),
    )
    add_fieldsets = (
        (
            "User Registration",
            {
                "classes": ("wide",),
                "fields": ("username", "email", "department", "password1", "password2"),
            },
        ),
    )

    def get_inlines(self, request, obj=None):
        if obj:
            return [ProfileInline]
        return []


admin.site.register(Department)
