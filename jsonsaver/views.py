from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView
from django.views.generic.edit import UpdateView

from . import forms
from .models import JsonStore


@login_required
def jsonsaver_root(request):
    return HttpResponseRedirect(reverse(settings.LOGIN_URL))


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
class JsonStoreDetailView(LoginRequiredMixin, DetailView):
    model = JsonStore
    # url_lookup_kwarg = 'store_pk'
    # pk_url_kwarg = 'jsonstore_pk'

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

    def test_func(self):
        return self.get_object().user == self.request.user


class JsonStoreNameDetailView(LoginRequiredMixin, DetailView):
    pass

    def test_func(self):
        return self.get_object().user == self.request.user


class JsonStorePublicNameDetailView(DetailView):
    pass


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
    success_message = "The '%(name)s' store has been deleted"
    success_url = reverse_lazy('users:user_detail')

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, self.success_message % obj.__dict__)
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        return self.get_object().user == self.request.user
