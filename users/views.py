from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.urls import reverse, reverse_lazy

from . import forms


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail'))


class UserRegisterView(SuccessMessageMixin, CreateView):
    form_class = forms.NewUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(settings.LOGIN_URL)
    success_message = "You have successfully registered your account."

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = AuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_message = "You are now logged in."


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail.html'

    def get_object(self):
        return self.request.user


class UserLogoutView(LogoutView):
    success_message = "You have successfully logged out."

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
