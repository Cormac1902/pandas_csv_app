from django.shortcuts import render
from django.http import HttpResponseRedirect as redirect
from .check_csv import check_rows, check_rows_by_column
from .load_csv import read_csv_file, get_headers
from .models import ColumnCheck


# Create your views here.
def csv_upload(request):
    return render(request, 'csv_upload.html', {})


# https://stackoverflow.com/questions/39003732/display-django-pandas-dataframe-in-a-django-template
def check_csv(request):
    if request.method == 'POST':
        csv_file = read_csv_file(request.FILES['file'])

        if request.POST['submit'] == 'Load headers':
            headers = {'headers': get_headers(csv_file)}
            return render(request, 'csv_upload.html', headers)
        elif request.POST['submit'] == 'Submit':
            checks = []

            for check in request.POST:
                if not (check == 'csrfmiddlewaretoken' or check == 'submit'):
                    checks.append(check)

            column_checks = {"workclass": ['Federal-gov', 'Local-gov', 'Never-worked', 'Private', 'Self-emp-inc',
                                           'Self-emp-not-inc', 'Without-pay']}

            ColumnCheck.objects.create(name='workclass',
                                       allowed_values=['Federal-gov', 'Local-gov', 'Never-worked', 'Private',
                                                       'Self-emp-inc', 'Self-emp-not-inc', 'Without-pay'])

            # column_checks_list = ColumnCheck.objects.all()
            # check_columns_against_allowed_values(csv_file, column_checks_list)

            errors = check_rows(csv_file, checks)

            ColumnCheck.objects.all().delete()

            return render(request, 'csv_results.html', {'errors': errors})

    return csv_upload(request)

# def csv_results(request, results):
#    return render(request, csv_results.html, results)
