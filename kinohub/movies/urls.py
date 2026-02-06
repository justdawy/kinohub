from django.urls import path

from movies import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "<slug:category_slug>/<slug:movie_slug>/",
        views.MovieDetailView.as_view(),
        name="movie_detail",
    ),
    path(
        "<slug:category_slug>/",
        views.CategoryDetailView.as_view(),
        name="category_detail",
    ),
]
