from django.http import HttpResponse

def project_root(request):
    return HttpResponse('Hello jsonsaver!')
