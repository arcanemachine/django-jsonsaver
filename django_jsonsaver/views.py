from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.urls import reverse
from django.shortcuts import render

from django.contrib.auth.decorators import user_passes_test
from .helpers import send_test_email
from django.http import HttpResponse
from users import tasks


def project_root(request):
    return render(request, 'project_root.html')


def project_root_api(request):
    return HttpResponse('Insert schema here.')


def user_is_staff(user):
    return user.is_staff


@user_passes_test(user_is_staff)
def test_email(request):
    # send_test_email('arcanemachine@gmail.com')
    tasks.send_test_email_task.delay('arcanemachine@gmail.com')
    return HttpResponse('sent?')
