from django.urls import path

from account.api import views

urlpatterns = [
    path("users/", views.UserApiView.as_view(), name="user-list"),
    path(
        "users/<int:pk>/profile/",
        views.ProfileEditApiView.as_view(),
        name="user-profile",
    ),
    path("users/<int:pk>/", views.UserEditApiView.as_view(), name="user-detail"),
    path(
        "users/<int:pk>/full",
        views.UserFullDetailApiView.as_view(),
        name="user-full-detail",
    ),
    path("users/stats/", views.UserStatsListApiView.as_view(), name="user-stats"),
]
