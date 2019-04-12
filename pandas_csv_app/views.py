from django.shortcuts import render
from django.http import HttpResponseRedirect as redirect
from .check_csv import check_rows, check_rows_by_column
from .load_csv import read_csv_file, get_headers, get_data_types
from .models import ColumnCheck
from .forms import ColumnCheckForm


# Create your views here.
def csv_upload(request):
    return render(request, 'csv_upload.html', {})


def check_csv(request):
    if request.method == 'POST':
        csv_file = read_csv_file(request.FILES['file'])

        if request.POST['submit'] == 'Load headers':

            ColumnCheck.objects.create(name='workclass', null_values=True,
                                       allowed_values=['Federal-gov', 'Local-gov', 'Never-worked', 'Private',
                                                       'Self-emp-inc', 'Self-emp-not-inc', 'Without-pay'])

            headers_dict = dict(zip(get_headers(csv_file), get_data_types(csv_file)))

            for header in headers_dict:
                dtype = str(headers_dict[header])
                headers_dict[header] = {'dtype': dtype, 'form': ColumnCheckForm({'name': header}, prefix=header)}

            ColumnCheck.objects.all().delete()
            form = ColumnCheckForm()

            return render(request, 'csv_upload_columns.html', {'headers_dict': headers_dict, 'file': csv_file, 'form' : form})
        elif request.POST['submit'] == 'Submit':
            checks = []

            for check in request.POST:
                if not (check == 'csrfmiddlewaretoken' or check == 'submit'):
                    checks.append(check)

            errors = check_rows(csv_file, checks)

            return render(request, 'csv_results.html', {'errors': errors})

    return csv_upload(request)


def check_csv_columns(request):
    if request.method == 'POST':

        for check in request.POST:
            if not (check == 'csrfmiddlewaretoken' or check == 'submit'):
                name = check.split('-')[0]
                print(name)
                try:
                    column_check = ColumnCheck.objects.get(name=name)
                except ColumnCheck.DoesNotExist:
                    column_check = ColumnCheck.objects.create(name=name)
                    pass

                if check.split('-')[1] == 'null_values':
                    column_check.null_values = True
                elif check.split('-')[1] == 'special_characters':
                    column_check.special_characters = True

        print(ColumnCheck.objects.all())
        return csv_upload(request)
