from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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


class JsonStoreDetailView(LoginRequiredMixin, DetailView):
    model = JsonStore

    def get_object(self):
        if self.kwargs.get('store_name'):
            return get_object_or_404(JsonStore, name=self.kwargs['store_name'])
        elif self.kwargs.get('store_pk'):
            return get_object_or_404(
                JsonStore,
                pk=self.kwargs['pk'],
                is_public=True)
