# from django.http import HttpResponseRedirect
# from django.urls import reverse
from django.shortcuts import render

# from django.http import HttpResponse
# from users.tasks import send_welcome_email_task


def project_root(request):
    return render(request, 'project_root.html')


# def test_email(request):
#     if not request.user.is_staff:
#         return HttpResponse('not sent')
#     send_welcome_email_task.delay('bob@email.com', '123')
#     return HttpResponse('sent?')
