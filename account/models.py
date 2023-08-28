from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class User(AbstractUser):
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        related_name="users",
        null=True,
        blank=True,
    )
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.username


class Profile(models.Model):
    GENDER_CHOICES = [
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Others", _("Others")),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=10000, null=True, blank=True)
    avatar = models.ImageField(upload_to="user/avatar", null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username
