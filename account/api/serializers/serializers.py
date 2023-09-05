import json
from datetime import datetime, timedelta

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.settings import api_settings

from account.models import Department, Profile, User
from api.serializers.serializers import DocumentListSerializer, ProjectListSerializer


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Department Model
    """

    class Meta:
        model = Department
        fields = ["id", "name"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for Profile Model
    """

    home_address = serializers.SerializerMethodField()

    def get_home_address(self, obj):
        if obj.home_address:
            home_address_dict = obj.home_address.geojson
            return json.loads(home_address_dict)
        return obj.home_address

    class Meta:
        model = Profile
        fields = ["bio", "avatar", "gender", "date_of_birth", "home_address"]

    def validate(self, attrs):
        date_of_birth = attrs["date_of_birth"]
        if date_of_birth:
            today = datetime.now().date()
            age = today - date_of_birth
            if age < timedelta(356 * 15):
                raise serializers.ValidationError(
                    {"date_of_birth": "Age must be more than 15 years old"}
                )
        if len(attrs["bio"]) > 10000:
            raise serializers.ValidationError("10000 character limit")
        return attrs


class BaseUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
            "password",
            "department",
            "profile",
        ]
        read_only_fields = [
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
            },
        }


class UserCreateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        pass

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", "")
        user = User.objects.create_user(**validated_data)
        profile = Profile.objects.get(user=user)
        profile.bio = profile_data.get("bio", "")
        profile.avatar = profile_data.get("avatar", "")
        profile.gender = profile_data.get("gender", "")
        profile.date_of_birth = profile_data.get("date_of_birth", "")
        profile.save()
        return user

    def validate(self, attrs):
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError("Email already exists")
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError("Username already exists")
        try:
            validate_password(
                password=attrs["password"],
                user=self.instance,
            )
        except ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        if len(attrs["profile"]["bio"]) > 10000:
            raise serializers.ValidationError("10000 character limit")
        date_of_birth = attrs["profile"]["date_of_birth"]
        if date_of_birth:
            today = datetime.now().date()
            age = today - date_of_birth
            if age < timedelta(356 * 15):
                raise serializers.ValidationError(
                    {"date_of_birth": "Age must be more than 15 years old"}
                )
        return attrs


class UserListSerializer(BaseUserSerializer):
    department = DepartmentSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        pass


class UserEditSerializer(BaseUserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
            "date_joined",
            "last_login",
            "department",
            "profile",
        ]

    def validate(self, attrs):
        instance = self.instance
        if (
            User.objects.filter(username=attrs["username"])
            .exclude(pk=instance.id)
            .exists()
        ):
            raise serializers.ValidationError("User with username already exists")
        if User.objects.filter(email=attrs["email"]).exclude(pk=instance.id).exists():
            raise serializers.ValidationError("User with email already exists")
        return attrs

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.department = validated_data.get("department", instance.department)
        instance.save()
        return instance


class UserFullSerializer(BaseUserSerializer):
    projects = ProjectListSerializer(many=True, read_only=True)
    files = DocumentListSerializer(many=True, read_only=True)
    department = serializers.StringRelatedField()

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + [
            "projects",
            "files",
        ]


class UserStatsListSerializer(BaseUserSerializer):
    no_of_projects = serializers.SerializerMethodField()
    no_of_files = serializers.SerializerMethodField()

    def get_no_of_files(self, obj):
        return obj.files.all().count()

    def get_no_of_projects(self, obj):
        return obj.projects.all().count()

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "username",
            "no_of_projects",
            "no_of_files",
            # "no_of_projects_month",
        ]
