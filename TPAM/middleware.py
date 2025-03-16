from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse, NoReverseMatch

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            try:
                # Include the namespace for the login route
                login_url = reverse('users:login')
            except NoReverseMatch:
                login_url = settings.LOGIN_URL

            if not request.path.startswith(login_url) and not request.path.startswith(settings.STATIC_URL):
                return redirect(f"{login_url}?next={request.path}")
        return self.get_response(request)