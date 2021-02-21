from django.contrib import messages
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DetailView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy

from . import forms
from django_jsonsaver import helpers

UserModel = get_user_model()


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail'))


class UserRegisterView(CreateView):
    form_class = forms.NewUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        messages.success(
            self.request, "Success! Please check your email inbox for "
            "your confirmation message.")
        helpers.send_welcome_email(user=self.object)
        return HttpResponseRedirect(self.get_success_url())


def user_confirm(request, confirmation_code):
    user = get_object_or_404(
        UserModel, profile__confirmation_code=confirmation_code)
    if user.is_active:
        messages.info(request, "Your account has already been confirmed.")
    user.is_active = True
    user.save()
    messages.success(request, "Account confirmed! You may now login.")
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = forms.UserAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_message = "You are now logged in."

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        temp_user = UserModel.objects.filter(username=username).first()
        if temp_user and not temp_user.is_active:
            messages.warning(
                request,
                "Your account has not been activated. "
                "Please check your email inbox for your activation email.")
        return super().post(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jsonstores'] = \
            self.get_object().jsonstore_set.order_by('-updated_at')
        return context

    def get_object(self):
        return self.request.user


class UserLogoutView(LogoutView):
    success_message = "You have successfully logged out."

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
