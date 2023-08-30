from django.urls import path

from api import views

urlpatterns = [
    path("documents/", views.DocumentListCreateApiView.as_view(), name="document-list"),
    path("documents/<pk>/", views.DocumentEditApiView.as_view(), name="document-edit"),
]
