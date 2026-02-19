from django.urls import include, path

from users.views import (
    AjaxLoginView,
    AjaxPasswordResetView,
    AjaxSignupView,
    create_review,
)

urlpatterns = [
    path("review/create/", create_review, name="review_add"),
    path("login/", AjaxLoginView.as_view(), name="login"),
    path("signup/", AjaxSignupView.as_view(), name="signup"),
    path(
        "password/reset/",
        AjaxPasswordResetView.as_view(),
        name="account_reset_password",
    ),
    path("", include("allauth.urls")),
]
