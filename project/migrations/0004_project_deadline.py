# Generated by Django 4.2.4 on 2023-09-04 07:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("project", "0003_document_uploaded_by"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="deadline",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]