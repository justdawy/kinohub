from django.urls import include, path

from users.views import (
    AjaxPasswordResetView,
    UserProfileTemplateView,
    profile_edit,
)

urlpatterns = [
    path(
        "password/reset/",
        AjaxPasswordResetView.as_view(),
        name="account_reset_password",
    ),
    path("profile/", UserProfileTemplateView.as_view(), name="account_profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    path("", include("allauth.urls")),
]
