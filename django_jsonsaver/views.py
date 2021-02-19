from django.shortcuts import render

def project_root(request):
    return render(request, 'project_root.html')
    # return HttpResponse('Hello jsonsaver!')
