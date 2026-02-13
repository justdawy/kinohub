from django.urls import include, path

from users.views import AjaxLoginView

urlpatterns = [
    path("login/", AjaxLoginView.as_view(), name="login"),
    path("", include("allauth.urls")),
]
