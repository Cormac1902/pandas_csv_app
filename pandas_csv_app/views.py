from django.shortcuts import render, redirect
from .check_csv import check_rows, check_rows_by_column
from .load_csv import read_csv_file, get_headers, get_data_types, count_records, count_unique_values, get_max, get_min
from .models import ColumnCheck
from .forms import ColumnCheckForm
from datetime import datetime

csv_file, headers_dict, filename = None, None, None


# Create your views here.
def csv_upload(request):
    return render(request, 'csv_upload.html', {})


def check_csv(request):
    if request.method == 'POST':
        global csv_file, filename
        csv_file = read_csv_file(request.FILES['file'])
        filename = request.FILES['file'].name

        if request.POST['submit'] == 'Load headers':

            headers = False
            if 'headers' in request.POST:
                headers = True

            null_values = False
            if 'null_values' in request.POST:
                null_values = True

            global headers_dict
            headers_dict = dict(zip(get_headers(csv_file), get_data_types(csv_file)))
            records = count_records(csv_file)

            for header in headers_dict:
                dtype = str(headers_dict[header])
                column = csv_file[header]
                headers_dict[header] = {'dtype': dtype,
                                        'records': count_records(csv_file, header),
                                        'unique_values': count_unique_values(column),
                                        'form': ColumnCheckForm(prefix=header)}
                if dtype == 'int64' or dtype == 'float64':
                    column_min, column_max = get_min(column), get_max(column)
                    headers_dict[header].update(
                        {'min': column_min, 'max': column_max,
                         'form': ColumnCheckForm(prefix=header, min_allowed=column_min, max_allowed=column_max)})
                elif dtype == 'datetime64':
                    headers_dict[header].update(
                        {'form': ColumnCheckForm(prefix=header, min_date_allowed=True, max_date_allowed=True)})

                ColumnCheck.objects.all().delete()

            return render(request, 'csv_upload_columns.html', {'headers_dict': headers_dict, 'filename': filename,
                                                               'headers': headers, 'null_values': null_values,
                                                               'records': records})
        elif request.POST['submit'] == 'Submit':
            checks = []

            for check in request.POST:
                if not (check == 'csrfmiddlewaretoken' or check == 'submit'):
                    checks.append(check)

            errors = check_rows(csv_file, checks)

            return render(request, 'csv_results.html', {'errors': errors, 'filename': filename})

    return redirect(csv_upload)


def check_csv_columns(request):
    if request.method == 'POST':
        global csv_file, headers_dict

        headers = False
        if 'headers' in request.POST:
            headers = True

        for check in request.POST:
            if not (check == 'csrfmiddlewaretoken' or check == 'submit' or check == 'headers'):
                name = check.split('-')[0]
                try:
                    column_check = ColumnCheck.objects.get(name=name)
                except ColumnCheck.DoesNotExist:
                    column_check = ColumnCheck.objects.create(name=name)

                if headers_dict[name]['dtype'] == 'int64' or headers_dict[name]['dtype'] == 'float64':
                    column = csv_file[name]
                    column_check.min = get_min(column)
                    column_check.max = get_max(column)
                elif headers_dict[name]['dtype'] == 'datetime64':
                    column = csv_file[name]
                    column_check.min_date = get_min(column)
                    column_check.max_date = get_max(column)

                if check.split('-')[1] == 'null_values':
                    column_check.null_values = True
                elif check.split('-')[1] == 'special_characters':
                    column_check.special_characters = True
                elif request.POST[check] is not '':
                    if check.split('-')[1] == 'min_allowed':
                        column_check.min_allowed = float(request.POST[check])
                    elif check.split('-')[1] == 'max_allowed':
                        column_check.max_allowed = float(request.POST[check])
                    elif check.split('-')[1] == 'min_date_allowed':
                        column_check.min_date_allowed = datetime.strptime(request.POST[check])
                    elif check.split('-')[1] == 'max_date_allowed':
                        column_check.max_date_allowed = datetime.strptime(request.POST[check])

                column_check.save()

        errors = check_rows_by_column(csv_file, headers)

        return render(request, 'csv_results.html', {'errors': errors, 'filename': filename})

    return redirect(csv_upload)
