# from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import FormView, TemplateView

from . import forms, helpers as h, tasks


def project_root(request):
    return render(request, 'project_root.html')


class ContactUsFormView(SuccessMessageMixin, FormView):
    template_name = 'contact_us.html'
    form_class = forms.ContactUsForm
    success_message = \
        "Your message has been received. Thank you for your feedback."

    def form_valid(self, form):
        name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']  # honeypot field
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        if not last_name:
            tasks.send_contact_us_email_task(name, email, message)
        return super().form_valid(form)

    def get_success_url(self):
        return h.get_next_url(self.request, '/')


class TermsOfUseTemplateView(TemplateView):
    template_name = 'terms_of_use.html'


class PrivacyPolicyTemplateView(TemplateView):
    template_name = 'privacy_policy.html'
