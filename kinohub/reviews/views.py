from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from movies.models import Movie

from .models import Like, Review


@require_POST
def create_review(request):
    movieId = request.POST.get("movieId")
    content = request.POST.get("content", "").strip()

    if not movieId or len(content) < 50:
        html = render_to_string(
            "movies/movie_detail.html#errors",
            {
                "errors": {
                    "content": ["Текст відгукa повинен містити не менше 50 символів"]
                }
            },
        )
        return HttpResponseBadRequest(html)

    try:
        movie = Movie.objects.get(id=movieId)
    except Movie.DoesNotExist:
        return HttpResponseBadRequest("Movie not found")

    if request.user.is_authenticated:
        if Review.objects.filter(
            user=request.user, movie=movie, parent__isnull=True
        ).exists():
            html = render_to_string(
                "movies/movie_detail.html#errors",
                {"errors": {"review": ["Ви вже залишили відгук до цього фільму"]}},
            )
            return HttpResponseBadRequest(html)

    review = Review(movie=movie, content=content)

    if request.user.is_authenticated:
        review.user = request.user
    else:
        review.guest_name = request.POST.get("guest_name", "Невідомий")

    review.save()

    messages.success(request, "Відгук успішно додано!")

    response = HttpResponse()
    response["HX-Redirect"] = request.META.get("HTTP_REFERER", "/")
    return response


def get_reviews(request, movie_id):
    page = request.GET.get("page", 1)
    movie_reviews = (
        Movie.objects.get(pk=movie_id)
        .reviews.filter(parent__isnull=True)
        .order_by("-created_on")
    )
    paginator = Paginator(movie_reviews, settings.REVIEW_PAGE_SIZE)
    context = {"movie_reviews": paginator.page(page)}
    return render(request, "movies/movie_detail.html#comments", context=context)


@login_required
def review_vote(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    content_type = ContentType.objects.get_for_model(Review)

    vote_type = request.POST.get("vote_type")
    if vote_type in ["like", "dislike"]:
        value = Like.LIKE if vote_type == "like" else Like.DISLIKE

        existing_vote = Like.objects.filter(
            user=request.user, content_type=content_type, object_id=review_id
        ).first()

        if existing_vote:
            if existing_vote.value == value:
                existing_vote.delete()
            else:
                existing_vote.value = value
                existing_vote.save()
        else:
            Like.objects.create(
                user=request.user,
                content_type=content_type,
                object_id=review_id,
                value=value,
            )

    return render(
        request,
        "movies/movie_detail.html#review_like_section",
        context={"review": review},
    )
