from django.urls import path

from reviews.views import create_review, get_reviews, review_vote

urlpatterns = [
    path("create/", create_review, name="review_add"),
    path("get-reviews/<int:movie_id>/", get_reviews, name="get_reviews"),
    path("vote/<int:review_id>/", review_vote, name="review_vote"),
]
