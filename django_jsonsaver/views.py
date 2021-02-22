from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


def project_root(request):
    if request.method == 'POST':
        if request.POST.get('search-public-store'):
            return HttpResponseRedirect(
                reverse('jsonsaver:jsonstore_detail_public', kwargs={
                    'jsonstore_name': request.POST['search-public-store']}))
    return render(request, 'project_root.html')
