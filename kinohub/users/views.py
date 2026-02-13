from allauth.account.views import LoginView
from django.http import JsonResponse


class AjaxLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.form_valid(form)
            return JsonResponse({"loggedIn": True})
        else:
            return JsonResponse({"loggedIn": False, "errors": form.errors})
