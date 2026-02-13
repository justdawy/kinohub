from django.urls import include, path

from users.views import AjaxLoginView, AjaxSignupView

urlpatterns = [
    path("login/", AjaxLoginView.as_view(), name="login"),
    path("signup/", AjaxSignupView.as_view(), name="signup"),
    path("", include("allauth.urls")),
]
