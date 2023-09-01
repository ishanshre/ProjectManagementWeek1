from rest_framework import serializers

from project.models import Document, Project


class BaseDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = [
            "uuid",
            "name",
            "document",
            "uploaded_at",
            "updated_at",
            "project",
            "uploaded_by",
        ]
        read_only_fields = ["uuid", "uploaded_at", "updated_at"]


class DocumentListSerializer(BaseDocumentSerializer):
    project = serializers.StringRelatedField()
    uploaded_by = serializers.StringRelatedField()
    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        return f"{obj.uploaded_by.department.name}"

    class Meta(BaseDocumentSerializer.Meta):
        fields = BaseDocumentSerializer.Meta.fields + ["department"]


class DocumentCreateSerializer(BaseDocumentSerializer):
    class Meta(BaseDocumentSerializer.Meta):
        pass

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        document = Document.objects.create(**validated_data)
        return document


class DocumentEditSerializer(BaseDocumentSerializer):
    class Meta(BaseDocumentSerializer.Meta):
        pass


class BaseProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_at",
            "updated_at",
            "user",
        ]
        read_only_fields = ["created_at", "updated_at"]


class ProjectListSerializer(BaseProjectSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta(BaseProjectSerializer.Meta):
        pass


class ProjectCreateSerializer(BaseProjectSerializer):
    class Meta(BaseProjectSerializer.Meta):
        pass

    def create(self, validated_data):
        project = Project.objects.create(**validated_data)
        return project


class ProjectEditSerializer(BaseProjectSerializer):
    class Meta(BaseProjectSerializer.Meta):
        pass


class ProjectDocSerializer(BaseProjectSerializer):
    documents = BaseDocumentSerializer(many=True, read_only=True)

    class Meta(BaseProjectSerializer.Meta):
        fields = BaseProjectSerializer.Meta.fields + ["documents"]
