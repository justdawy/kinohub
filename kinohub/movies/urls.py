from django.urls import path
from django.views.generic import TemplateView

from movies import views

urlpatterns = [
    path("", TemplateView.as_view(template_name="movies/index.html"), name="index"),
    path("abuse/", views.AbuseTemplateView.as_view(), name="abuse"),
    path("search/", views.SearchListView.as_view(), name="search"),
    path(
        "<slug:category_slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
    path(
        "<slug:category_slug>/<int:id>-<slug:movie_slug>/",
        views.MovieDetailView.as_view(),
        name="movie_detail",
    ),
    path(
        "actors/<slug:actor_slug>", views.ActorDetailView.as_view(), name="actor_detail"
    ),
]
