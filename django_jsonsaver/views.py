from django.http import HttpResponse  # , HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.views.generic import FormView

from . import forms, tasks

# from django.contrib.auth.decorators import user_passes_test
# from django.http import HttpResponse
# from . import helpers as h
# from . import tasks


def project_root(request):
    return render(request, 'project_root.html')


class ContactUsFormView(SuccessMessageMixin, FormView):
    template_name = 'contact_us.html'
    form_class = forms.ContactUsForm
    success_url = '/'
    success_message = \
        "Your message has been received. Thank you for your feedback."

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message = form.cleaned_data['message']
        # h.send_contact_us_email(name, email, message)
        tasks.send_contact_us_email_task(name, email, message)
        return super().form_valid(form)


# def test_func_user_is_staff(user):
#     return user.is_staff
#
#
# @user_passes_test(test_func_user_is_staff)
# def test_email(request):
#     # h.send_test_email('arcanemachine@gmail.com')
#     tasks.send_test_email_task.delay('arcanemachine@gmail.com')
#     return HttpResponse('sent?')
