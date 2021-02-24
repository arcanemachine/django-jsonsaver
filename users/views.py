from django.contrib import messages
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, FormView, DeleteView, DetailView,\
    TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from rest_framework.authtoken.models import Token

from . import forms
from .models import Profile
from .tasks import send_welcome_email_task
from django_jsonsaver import helpers
from jsonsaver.models import JsonStore

UserModel = get_user_model()


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail_me'))


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

        user = self.object
        send_welcome_email_task.delay(
            user.email, user.username, user.profile.activation_code)
        if settings.DEBUG:
            helpers.send_welcome_email(
                user.email, user.username, user.profile.activation_code)
        messages.success(
            self.request, "Success! Please check your email inbox for "
            "your confirmation message.")
        return HttpResponseRedirect(self.get_success_url())


class UserActivationEmailResend(FormView):
    template_name = 'users/user_activation_email_resend.html'
    form_class = forms.UserActivationEmailResendForm

    def form_valid(self, form):
        user = \
            UserModel.objects.filter(email=form.cleaned_data['email']).first()
        if user and user.is_active:
            messages.info(
                self.request, "This account has already been activated.")
            return HttpResponseRedirect(reverse(settings.LOGIN_URL))
        if user and not user.is_active:
            # resend the welcome email
            send_welcome_email_task.delay(
                user.email, user.username, user.profile.activation_code)
            if settings.DEBUG:
                helpers.send_welcome_email(
                    user.email, user.username, user.profile.activation_code)
        messages.success(
            self.request, "If the email address you entered "
            "matches an account that has not yet been activated, "
            "then we have resent an activation email to that address.")
        return HttpResponseRedirect(reverse('users:login'))


def user_activate(request, activation_code):
    user = get_object_or_404(
        UserModel, profile__activation_code=activation_code)
    if user.is_active:
        messages.info(request, "Your account has already been activated.")
        return HttpResponseRedirect(reverse(settings.LOGIN_URL))
    user.is_active = True
    user.save()
    Token.objects.get_or_create(user=user)
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
            return HttpResponseRedirect(
                reverse('users:user_activation_email_resend'))
        return super().post(request, *args, **kwargs)


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_jsonstores = JsonStore.objects.filter(user=self.request.user)
        context.update({
            'jsonstores': user_jsonstores.order_by('-updated_at')[:5],
            'user_jsonstores_count': user_jsonstores.count(),
            'user_token': Token.objects.get(user=self.request.user)})
        return context

    def get_object(self):
        return self.request.user


class UserDetailPublicView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail_public.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_jsonstores = JsonStore.objects.filter(
            user=self.get_object(),
            is_public=True)
        context.update({
            'public_user': self.get_object(),
            'jsonstores': user_jsonstores.order_by('-updated_at')[:5]})
        return context

    def get_object(self):
        user = get_object_or_404(UserModel, username=self.kwargs['username'])
        if user.profile.is_public:
            return user
        else:
            raise Http404


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ('is_public',)
    template_name = 'users/user_profile_update.html'

    def get_object(self):
        return self.request.user.profile


class UserApiKeyResetView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_api_key_reset.html'

    def post(self, request, *args, **kwargs):
        old_token = Token.objects.get(user=request.user)
        old_token.delete()
        new_token = Token.objects.create(user=request.user)
        messages.success(request, f"Your new API key is '{new_token.key}'")
        return HttpResponseRedirect(reverse('users:user_detail_me'))


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('project_root')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Your account has been deleted.")
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class UserLogoutView(LogoutView):
    success_message = "You have successfully logged out."

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
