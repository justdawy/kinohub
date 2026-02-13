from allauth.account.views import LoginView, SignupView
from django.http import JsonResponse


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
