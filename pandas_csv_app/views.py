from django.shortcuts import render

# Create your views here.


def csv_upload(request):
    return render(request, 'pandas_csv_app/csv_upload.html', {})
