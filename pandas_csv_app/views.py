from django.shortcuts import render
from django.http import HttpResponseRedirect
import 1 as check

# Create your views here.


def csv_upload(request):
    return render(request, 'csv_upload.html', {})


def check_csv(request):
    if request.method == 'POST':
        check.check_data(request.FILES['file'])
        return HttpResponseRedirect('/success/url/')

    return csv_upload()
