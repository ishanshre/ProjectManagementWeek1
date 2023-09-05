# Generated by Django 4.2.4 on 2023-09-05 05:02

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_project_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site', models.CharField(max_length=100)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('area', django.contrib.gis.db.models.fields.PolygonField(blank=True, null=True, srid=4326)),
                ('way', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to='project.project')),
            ],
        ),
    ]