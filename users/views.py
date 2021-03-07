from django.contrib import messages
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect  # , HttpResponse
from django.views.generic import CreateView, FormView, DeleteView, DetailView,\
    TemplateView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from rest_framework.authtoken.models import Token

from . import forms
from .models import Profile
from django_jsonsaver import constants as c, helpers as h
from django_jsonsaver import tasks
from stores.models import JsonStore

UserModel = get_user_model()


def users_root(request):
    return HttpResponseRedirect(reverse('users:user_detail_me'))


class UserRegisterView(CreateView):
    form_class = forms.NewUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # do not process form if honeypot field filled (name)
        if form.cleaned_data.get('name', None):
            self.object = None
            return HttpResponseRedirect(self.success_url)
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()

        user = self.object
        tasks.send_welcome_email_task.delay(
            user.email, user.profile.activation_code)
        if settings.DEBUG:
            h.send_welcome_email(
                user.email, user.profile.activation_code)
        messages.success(self.request, c.USER_VIEW_REGISTER_SUCCESS_MESSAGE)
        return HttpResponseRedirect(self.success_url)


class UserActivationEmailResendView(FormView):
    template_name = 'users/user_activation_email_resend.html'
    form_class = forms.UserActivationEmailResendForm
    success_url = reverse_lazy(settings.LOGIN_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = \
            UserModel.objects.filter(email=form.cleaned_data['email']).first()
        # notify user if account is already active
        if user and user.is_active:
            messages.info(
                self.request,
                c.USER_VIEW_ACTIVATION_EMAIL_RESEND_ACCOUNT_ALREADY_ACTIVE)
            return HttpResponseRedirect(reverse(settings.LOGIN_URL))
        # if account exists and is not active, resend welcome email
        if user and not user.is_active:
            tasks.send_welcome_email_task.delay(
                user.email, user.profile.activation_code)
            if settings.DEBUG:
                h.send_welcome_email(
                    user.email, user.profile.activation_code)
        messages.success(
            self.request, c.USER_VIEW_ACTIVATION_EMAIL_RESEND_SUCCESS_MESSAGE)
        return HttpResponseRedirect(self.success_url)


def user_activate(request, activation_code):
    success_url = reverse(settings.LOGIN_URL)

    # activate user
    user = get_object_or_404(
        UserModel, profile__activation_code=activation_code)
    if user.is_active or request.user.is_authenticated:
        messages.info(
            request, c.USER_VIEW_USER_ACTIVATE_ACCOUNT_ALREADY_ACTIVE)
        return HttpResponseRedirect(success_url)
    user.is_active = True
    user.save()

    # generate an API token for the user
    Token.objects.create(user=user)

    # remove activation code from profile
    user.profile.activation_code = None
    user.profile.save()

    # show success_message and redirect to success_url
    messages.success(request, c.USER_VIEW_USER_ACTIVATE_SUCCESS_MESSAGE)
    return HttpResponseRedirect(success_url)


class UserLoginView(SuccessMessageMixin, LoginView):
    form_class = forms.UserAuthenticationForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_message = c.USER_VIEW_LOGIN_SUCCESS_MESSAGE

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        temp_user = UserModel.objects.filter(username=username).first()
        if temp_user and not temp_user.is_active:
            messages.warning(
                request, c.USER_VIEW_LOGIN_ACTIVATE_ACCOUNT_REMINDER)
            return HttpResponseRedirect(
                reverse('users:user_activation_email_resend'))
        return super().post(request, *args, **kwargs)


class UserUsernameRecoverView(FormView):
    form_class = forms.UserUsernameRecoverForm
    template_name = 'users/user_username_recover.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = UserModel.objects.filter(email=email).first()

        if user:
            tasks.send_user_username_recover_email_task.delay(
                email, user.username)
            if settings.DEBUG:
                h.send_user_username_recover_email(email, user.username)
        messages.success(
            self.request, "If a user account exists with that email address, "
            "then we have sent them an email containing their username.")
        return HttpResponseRedirect(reverse('users:login'))


class UserLogoutView(LogoutView):
    success_message = c.USER_VIEW_LOGOUT_SUCCESS_MESSAGE

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)


class UserDetailMeView(LoginRequiredMixin, DetailView):
    template_name = 'users/user_detail_me.html'

    def get_object(self):
        return self.request.user


class UserDetailPublicView(DetailView):
    template_name = 'users/user_detail_public.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object().profile.is_public:
            if request.user == self.get_object():
                messages.info(
                    request, c.USER_VIEW_DETAIL_PUBLIC_SAME_USER_IS_PRIVATE)
                return HttpResponseRedirect(
                    reverse('users:user_update_is_public'))
            else:
                raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_jsonstores = JsonStore.objects.filter(
            user=self.get_object(),
            is_public=True).order_by('-updated_at')
        context.update({'jsonstores': user_jsonstores})
        return context

    def get_object(self):
        return get_object_or_404(UserModel, username=self.kwargs['username'])


class UserUpdateTemplateView(
        LoginRequiredMixin, SuccessMessageMixin, TemplateView):
    model = Profile
    template_name = 'users/user_update.html'


class UserUpdateAccountTierView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_update_account_tier.html'


class UserUpdateEmailView(LoginRequiredMixin, FormView):
    form_class = forms.UserUpdateEmailForm
    template_name = 'users/user_update_email.html'
    success_url = reverse_lazy('users:user_detail_me')

    def form_valid(self, form):
        user = self.request.user
        profile = self.get_object()
        email = form.cleaned_data['email']

        # update profile
        profile.wants_email = email
        profile.activation_code = Token().generate_key()
        profile.save()

        # send confirmation email
        tasks.send_email_update_email_task.delay(
            email, user.profile.activation_code)
        if settings.DEBUG:
            h.send_email_update_email(email, user.profile.activation_code)
        messages.success(
            self.request, c.USER_VIEW_UPDATE_EMAIL_SUCCESS_MESSAGE)

        return HttpResponseRedirect(self.success_url)

    def get_object(self):
        return self.request.user.profile


@login_required
def user_update_email_confirm(request, activation_code):
    user = get_object_or_404(
        UserModel, profile__activation_code=activation_code)

    user.email = user.profile.wants_email
    user.save()

    user.profile.wants_email = None
    user.profile.activation_code = None
    user.profile.save()

    messages.success(
        request, c.USER_VIEW_UPDATE_EMAIL_CONFIRM_SUCCESS_MESSAGE(user.email))
    return HttpResponseRedirect(reverse('users:user_detail_me'))


class UserUpdateIsPublicView(
        LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    fields = ('is_public',)
    template_name = 'users/user_update_is_public.html'
    success_message = c.USER_VIEW_UPDATE_IS_PUBLIC_SUCCESS_MESSAGE
    success_url = reverse_lazy('users:user_detail_me')

    def get_object(self):
        return self.request.user.profile


class UserUpdateApiKeyView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_update_api_key.html'
    success_url = reverse_lazy('users:user_detail_me')

    def post(self, request, *args, **kwargs):
        old_token = request.user.auth_token
        old_token.delete()
        new_token = Token.objects.create(user=request.user)
        messages.success(
            request, c.USER_VIEW_UPDATE_API_KEY_SUCCESS_MESSAGE(new_token.key))
        return HttpResponseRedirect(self.success_url)


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'users/user_delete.html'
    success_url = reverse_lazy('project_root')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, c.USER_VIEW_DELETE_SUCCESS_MESSAGE)
        return super().delete(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
