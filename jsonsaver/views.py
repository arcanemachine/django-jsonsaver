from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from . import forms
from .models import JsonStore


@login_required
def jsonsaver_root(request):
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))


class JsonStoreCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JsonStore
    template_name = 'jsonsaver/jsonstore_create.html'
    form_class = forms.JsonStoreForm
    success_message = "JSON Store created: %(name)s"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class JsonStoreDetailView(LoginRequiredMixin, DetailView):
    model = JsonStore
    url_lookup_kwarg = 'store_pk'

    def get_object(self):
        user = self.request.user
        if self.kwargs.get('jsonstore_pk'):
            obj = get_object_or_404(JsonStore, pk=self.kwargs['jsonstore_pk'])
        elif self.kwargs.get('jsonstore_name'):
            obj = get_object_or_404(
                JsonStore, name=self.kwargs['jsonstore_name'], user=user)
        if user.is_staff or obj.is_public or obj.user == user:
            return obj
        else:
            raise PermissionDenied
