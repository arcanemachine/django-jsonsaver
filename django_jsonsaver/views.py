from django.shortcuts import render

# from django.http import HttpResponse
# from django.contrib.auth import get_user_model
# from django_jsonsaver import helpers
# from django.core.mail import send_mail


def project_root(request):
    return render(request, 'project_root.html')


# def test_email(request):
#     helpers.send_welcome_email(get_user_model().objects.first())
#     return HttpResponse('sent?')
