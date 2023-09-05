from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as geomodels
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


class Profile(geomodels.Model):
    GENDER_CHOICES = [
        ("Male", _("Male")),
        ("Female", _("Female")),
        ("Others", _("Others")),
    ]
    user = geomodels.OneToOneField(
        User, on_delete=geomodels.CASCADE, related_name="profile"
    )
    bio = geomodels.TextField(max_length=10000, null=True, blank=True)
    avatar = geomodels.ImageField(upload_to="user/avatar", null=True, blank=True)
    date_of_birth = geomodels.DateField(null=True, blank=True)
    gender = geomodels.CharField(max_length=6, choices=GENDER_CHOICES)
    home_address = geomodels.PointField(null=True, blank=True)

    def __str__(self):
        return self.user.username
