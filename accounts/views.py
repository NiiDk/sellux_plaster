"""
Views for accounts app: registration, login, logout, profile.

We favor class-based views (CBVs). Authentication flow:
- Registration: `RegisterView` creates a new `CustomUser` then redirects to login.
- Login/Logout: Use Django's built-in `LoginView` and `LogoutView` for secure
  session handling.
- Profile: `ProfileView` requires authentication and allows updating profile fields.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import CustomUserCreationForm, ProfileUpdateForm

User = get_user_model()


class RegisterView(CreateView):
    """Self-service registration view.

    Uses `CustomUserCreationForm`. On successful registration users are
    redirected to the login page. In production you might want to send a
    confirmation email before allowing login.
    """

    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')


class LoginView(auth_views.LoginView):
    """Django's built-in login view with our template."""

    template_name = 'accounts/login.html'

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('dashboard:admin_intel')
        return reverse_lazy('dashboard:home')


class LogoutView(auth_views.LogoutView):
    """Logout view; uses `LOGOUT_REDIRECT_URL` from settings."""

    pass


class ProfileView(LoginRequiredMixin, UpdateView):
    """Authenticated profile view for updating user fields.

    `get_object` returns the currently logged-in user. Using `LoginRequiredMixin`
    ensures only authenticated users can access this view.
    """

    model = User
    template_name = 'accounts/profile.html'
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user
