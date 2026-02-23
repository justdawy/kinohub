from allauth.account.views import LoginView, PasswordResetView, SignupView
from django.contrib import messages
from django.http import HttpResponseNotAllowed, JsonResponse
from django.views.generic import TemplateView
from movies.models import Movie, Review


def create_review(request):
    if request.method == "POST":
        movieId = request.POST.get("movieId")
        content = request.POST.get("content")
        if movieId and content:
            try:
                movie = Movie.objects.get(id=movieId)
                review = Review(movie=movie, content=content)
                if request.user.is_authenticated:
                    review.user = request.user
                else:
                    review.guest_name = request.POST.get("guest_name")
                review.save()
                return JsonResponse({"created": True})
            except Exception:
                return JsonResponse({"created": False})
    return HttpResponseNotAllowed(request)


class AjaxFormMixin:
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            return JsonResponse({"loggedIn": True})
        return JsonResponse({"loggedIn": False, "errors": form.errors}, status=400)


class AjaxLoginView(AjaxFormMixin, LoginView):
    pass


class AjaxSignupView(AjaxFormMixin, SignupView):
    pass


class AjaxPasswordResetView(PasswordResetView):
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.form_valid(form)
            messages.add_message(
                request,
                messages.INFO,
                (
                    f"Лист для зміни пароля було надіслано на адресу "
                    f"{form.cleaned_data['email']}"
                ),
            )
        return JsonResponse({"emailSent": True})


class UserProfileTemplateView(TemplateView):
    template_name = "users/profile.html"
