from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, TemplateView

from . import constants as c, helpers as h
from . import forms, tasks


class ProjectRootTemplateView(TemplateView):
    template_name = 'project_root.html'


class ContactUsFormView(SuccessMessageMixin, FormView):
    template_name = 'contact_us.html'
    form_class = forms.ContactUsForm
    success_message = c.DJANGO_JSONSAVER_CONTACT_US_FORM_SUCCESS_MESSAGE

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


class FaqTemplateView(TemplateView):
    template_name = 'faq.html'


class PrivacyPolicyTemplateView(TemplateView):
    template_name = 'privacy_policy.html'


class TermsOfUseTemplateView(TemplateView):
    template_name = 'terms_of_use.html'
