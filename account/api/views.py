from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.filters import stats_filter
from account.api.serializers.serializers import (
    BaseUserSerializer,
    DepartmentSerializer,
    ProfileSerializer,
    UserCreateSerializer,
    UserEditSerializer,
    UserFullSerializer,
    UserListSerializer,
    UserStatsListSerializer,
)
from account.models import Department, Profile, User


class UserApiView(generics.ListCreateAPIView):
    serializer_class = BaseUserSerializer
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        user = User.objects.all()
        serializer = UserListSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserEditApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserEditSerializer
    queryset = User.objects.all()


class ProfileEditApiView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()


class UserFullDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        user = User.objects.get(pk=pk)
        serializer = UserFullSerializer(user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserStatsListApiView(generics.ListAPIView):
    serializer_class = UserStatsListSerializer
    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter,
        SearchFilter,
    ]
    filterset_class = stats_filter.UserStatFilter
    ordering_fields = [
        "username",
        "projects__created_at",
        "no_of_projects",
        "no_of_files",
    ]
    search_fields = ["=username"]

    def get_queryset(self):
        return User.objects.prefetch_related("projects", "files").annotate(
            no_of_projects=Count("projects"),
            no_of_files=Count("files"),
        )
