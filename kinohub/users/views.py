from allauth.account.models import EmailAddress
from allauth.account.views import LoginView, PasswordResetView, SignupView
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from movies.models import Movie, Review


@require_POST
def create_review(request):
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
        except Exception:
            pass
    movie_reviews = Review.objects.filter(
        movie__id=movieId, parent__isnull=True
    ).order_by("-created_on")
    return render(
        request,
        template_name="movies/movie_detail.html#comments",
        context={"movie_reviews": movie_reviews},
    )


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


class UserProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "users/profile.html"


@login_required
@require_POST
def profile_edit(request):
    user = request.user
    errors = {}

    email = request.POST.get("email", "").strip()
    old_password = request.POST.get("oldPassword", "")
    new_password = request.POST.get("newPassword", "")
    confirm_new_password = request.POST.get("confirmNewPassword", "")
    if request.FILES.get("profile_image"):
        if (
            user.profile_image
            and user.profile_image.name != "images/default-avatar.png"
        ):
            user.profile_image.delete(save=False)

        user.profile_image = request.FILES["profile_image"]
        user.save()
    if request.POST.get("deleteAvatar") == "true":
        if (
            user.profile_image
            and user.profile_image.name != "images/default-avatar.png"
        ):
            user.profile_image.delete(save=False)

        user.profile_image = user._meta.get_field("profile_image").get_default()
        user.save()
    if email and email != user.email:
        try:
            validate_email(email)

            if (
                EmailAddress.objects.filter(email__iexact=email)
                .exclude(user=user)
                .exists()
            ):
                errors.setdefault("email", []).append(
                    "Ця електронна пошта вже використовується."
                )
            else:
                user.email = email
                user.save()

                email_obj = EmailAddress.objects.filter(user=user, primary=True).first()
                if email_obj:
                    email_obj.email = email
                    email_obj.verified = False
                    email_obj.save()
                else:
                    EmailAddress.objects.create(
                        user=user, email=email, primary=True, verified=False
                    )

        except ValidationError:
            errors.setdefault("email", []).append(
                "Введіть коректну адресу електронної пошти."
            )

    if old_password or new_password or confirm_new_password:
        if not old_password:
            errors.setdefault("oldPassword", []).append("Введіть поточний пароль.")
        elif not user.check_password(old_password):
            errors.setdefault("oldPassword", []).append("Неправильний поточний пароль.")

        if new_password != confirm_new_password:
            errors.setdefault("confirmNewPassword", []).append(
                "Нові паролі не співпадають."
            )

        if new_password:
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                errors.setdefault("newPassword", []).extend(e.messages)

        if not errors and new_password:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

    if errors:
        return JsonResponse({"success": False, "errors": errors})

    messages.add_message(request, messages.SUCCESS, "Профіль успішно оновлено")

    return JsonResponse({"success": True})
