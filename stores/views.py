from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DetailView, DeleteView, FormView,\
    ListView
from django.views.generic.edit import UpdateView

from . import forms
from .models import JsonStore
from .permissions import UserHasJsonStorePermissionsMixin
from django_jsonsaver import constants as c


class JsonStoreListView(LoginRequiredMixin, ListView):
    model = JsonStore
    context_object_name = 'jsonstores'
    paginate_by = c.JSONSTORE_LIST_PAGINATE_BY

    def get_queryset(self):
        return self.request.user.jsonstore_set.order_by('-updated_at')


class JsonStoreCreateView(LoginRequiredMixin, CreateView):
    model = JsonStore
    form_class = forms.JsonStoreForm
    success_message = c.JSONSTORE_CREATE_SUCCESS_MESSAGE

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
        messages.success(
            self.request, self.success_message,
            extra_tags='jsonstore-create-success')
        return HttpResponseRedirect(self.get_success_url())


class JsonStoreDetailView(UserHasJsonStorePermissionsMixin, DetailView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'


class JsonStoreLookupView(LoginRequiredMixin, FormView):
    form_class = forms.JsonStoreLookupForm
    template_name = 'stores/jsonstore_lookup.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse('stores:jsonstore_detail_name', kwargs={
                'jsonstore_name': form.cleaned_data['jsonstore_name']}))


class JsonStoreNameDetailView(
        LoginRequiredMixin, UserHasJsonStorePermissionsMixin, DetailView):
    model = JsonStore

    def dispatch(self, request, *args, **kwargs):
        if self.get_object() is None:
            messages.error(
                request, "You do not have a JSON store with that name.")
            return HttpResponseRedirect(
                reverse('stores:jsonstore_lookup'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return JsonStore.objects.filter(
            user__id=self.request.user.id,
            name=self.kwargs['jsonstore_name']
        ).first()


class JsonStorePublicDetailView(DetailView):
    model = JsonStore

    def dispatch(self, request, *args, **kwargs):
        if not self.get_object():
            messages.error(
                request,
                "We could not find a public JSON store with that name.")
            return HttpResponseRedirect(
                reverse('stores:jsonstore_lookup_public'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        return JsonStore.objects.filter(
            name=self.kwargs['jsonstore_name']).first()


class JsonStorePublicLookupView(FormView):
    form_class = forms.JsonStorePublicLookupForm
    template_name = 'stores/jsonstore_lookup.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse('stores:jsonstore_detail_public', kwargs={
                'jsonstore_name': form.cleaned_data['jsonstore_name']}))


class JsonStoreUpdateView(
        UserHasJsonStorePermissionsMixin, SuccessMessageMixin, UpdateView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'
    form_class = forms.JsonStoreForm
    success_message = c.JSONSTORE_UPDATE_SUCCESS_MESSAGE

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action_verb'] = 'Update'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user,
                       'obj': self.get_object()})
        return kwargs


# delete
class JsonStoreDeleteView(UserHasJsonStorePermissionsMixin, DeleteView):
    model = JsonStore
    pk_url_kwarg = 'jsonstore_pk'
    success_message = c.JSONSTORE_DELETE_SUCCESS_MESSAGE
    success_url = reverse_lazy('stores:jsonstore_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message,
            extra_tags='jsonstore-delete-success')
        return super().delete(request, *args, **kwargs)
