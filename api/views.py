from django_filters import rest_framework as drf_filters
from rest_framework import filters, generics, mixins, status
from rest_framework.response import Response

from api.filters.filters import DocumentFilter
from api.serializers.serializers import (
    BaseDocumentSerializer,
    BaseProjectSerializer,
    DocumentCreateSerializer,
    DocumentEditSerializer,
    DocumentListSerializer,
    ProjectCreateSerializer,
    ProjectDocSerializer,
    ProjectEditSerializer,
    ProjectListSerializer,
)
from project.models import Document, Project


class DocumentListCreateApiView(generics.ListCreateAPIView):
    queryset = Document.objects.all()
    filter_backends = [
        drf_filters.DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = ["name", "uuid", "uploaded_by", "updated_by"]
    filterset_class = DocumentFilter
    serializer_class = DocumentListSerializer

    # def get(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(self.get_queryset(), many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = DocumentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DocumentEditApiView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = BaseDocumentSerializer
    queryset = Document.objects.all()

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ProjectListCreateApiView(generics.GenericAPIView):
    serializer_class = BaseProjectSerializer
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = ProjectListSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectEditApiView(mixins.DestroyModelMixin, generics.GenericAPIView):
    serializer_class = BaseProjectSerializer
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        serializer = ProjectDocSerializer(self.get_object())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer = ProjectCreateSerializer(self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
