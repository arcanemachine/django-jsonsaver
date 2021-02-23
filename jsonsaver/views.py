from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, ListView
from django.views.generic.edit import UpdateView

from . import forms
from .models import JsonStore
from django_jsonsaver import constants as c


@login_required
def jsonsaver_root(request):
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))


# list
class JsonStoreListView(LoginRequiredMixin, ListView):
    model = JsonStore
    context_object_name = 'jsonstores'
    paginate_by = c.JSONSTORE_PAGINATE_BY

    def get_queryset(self):
        return JsonStore.objects.filter(user=self.request.user) \
            .order_by('-updated_at')


# create
class JsonStoreCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = JsonStore
    form_class = forms.JsonStoreForm
    success_message = "Store created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_verb'] = 'Create'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# detail
class JsonStoreDetailView(UserPassesTestMixin, DetailView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'

    def test_func(self):
        return self.get_object().user == self.request.user


class JsonStoreNameDetailView(LoginRequiredMixin, DetailView):
    model = JsonStore

    def get_object(self):
        return get_object_or_404(
            JsonStore,
            name=self.kwargs['jsonstore_name'],
            user=self.request.user)

    def test_func(self):
        return self.get_object().user == self.request.user


class JsonStorePublicNameDetailView(DetailView):
    model = JsonStore

    def get_object(self):
        return get_object_or_404(JsonStore, name=self.kwargs['jsonstore_name'])

    def test_func(self):
        return self.get_object().user == self.request.user


# update
class JsonStoreUpdateView(
        UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'
    form_class = forms.JsonStoreForm
    success_message = "Store updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_verb'] = 'Update'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        kwargs['obj'] = self.get_object()
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.get_object().user == self.request.user


# delete
class JsonStoreDeleteView(UserPassesTestMixin, DeleteView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'
    success_message = "This store has been deleted."
    success_url = reverse_lazy('jsonsaver:jsonstore_list')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().user == self.request.user
