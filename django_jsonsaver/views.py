from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# from django.http import HttpResponse
# from users.tasks import send_welcome_email_task

from . import forms


def project_root(request):
    form = forms.JsonStorePublicSearchForm()
    if request.method == 'POST':
        form = forms.JsonStorePublicSearchForm(request.POST)
        if request.POST.get('jsonstore_public_name'):
            return HttpResponseRedirect(
                reverse('jsonsaver:jsonstore_detail_public', kwargs={
                    'jsonstore_name': request.POST['jsonstore_public_name']}))
    context = {
        'form': form,
        'cancel_button': False}
    return render(request, 'project_root.html', context)


# def test_email(request):
#     if not request.user.is_staff:
#         return HttpResponse('not sent')
#     send_welcome_email_task.delay('bob@email.com', '123')
#     return HttpResponse('sent?')
