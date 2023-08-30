from django.urls import path

from account.api import views

urlpatterns = [
    path("auth/users/", views.UserApiView.as_view(), name="user-list"),
    path(
        "auth/users/<int:pk>/profile/",
        views.ProfileEditApiView.as_view(),
        name="user-profile",
    ),
    path("auth/users/<int:pk>/", views.UserEditApiView.as_view(), name="user-detail"),
    path(
        "auth/users/<int:pk>/full",
        views.UserFullDetailApiView.as_view(),
        name="user-full-detail",
    ),
]
