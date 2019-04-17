from django.shortcuts import render, redirect
from .check_csv import check_rows, check_rows_by_column, update_regex
from .load_csv import read_csv_file, get_headers, get_data_types, count_records, count_unique_values, get_max, \
    get_min, get_unique_values
from .models import ColumnCheck
from .forms import ColumnCheckForm

csv_file, headers_dict, filename = None, None, None


# Create your views here.
def csv_upload(request, error=None):
    return render(request, 'csv_upload.html',
                  {'missing_values': ["N/A", "N/a", "n/A", "n/a", "Na", "nA", "na", "---", "--", "-", "?", " "],
                   'error': error})


def check_csv(request):
    if request.method == 'POST':
        global csv_file, filename
        csv_file = read_csv_file(request.FILES['file'], request.POST.getlist('missing-values'))

        if csv_file is False:
            return csv_upload(request, 'CSV file was blank')

        filename = request.FILES['file'].name

        if request.POST['regex']:
            update_regex(request.POST['regex'])
        else:
            update_regex('(?![a-zA-ZÀ-ÿ0-9-_<>=]).')

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
                elif dtype == 'object':
                    unique_values = get_unique_values(csv_file[header].dropna())
                    headers_dict[header].update(
                        {'form': ColumnCheckForm(prefix=header,
                                                 allowed_values=unique_values)})

                ColumnCheck.objects.all().delete()

            return render(request, 'csv_upload_columns.html', {'headers_dict': headers_dict, 'filename': filename,
                                                               'headers': headers, 'null_values': null_values,
                                                               'records': records})
        elif request.POST['submit'] == 'Submit':
            checks = []

            for check in request.POST:
                if not (check == 'csrfmiddlewaretoken' or check == 'submit' or check == 'regex'):
                    checks.append(check)

            errors = check_rows(csv_file, checks)

            return render(request, 'csv_results.html', {'errors': errors, 'filename': filename})

    return redirect(csv_upload)


def check_csv_columns(request):
    if request.method == 'POST':
        global csv_file, headers_dict

        if headers_dict:
            headers = False
            if 'headers' in request.POST:
                headers = True

            for header in headers_dict:
                try:
                    ColumnCheck.objects.get(name=header)
                except ColumnCheck.DoesNotExist:
                    ColumnCheck.objects.create(name=header)

            for column_check in ColumnCheck.objects.all():
                if headers_dict[column_check.name]['dtype'] == 'int64' \
                        or headers_dict[column_check.name]['dtype'] == 'float64':
                    column = csv_file[column_check.name]
                    column_check.min = get_min(column)
                    column_check.max = get_max(column)
                elif headers_dict[column_check.name]['dtype'] == 'datetime64':
                    column = csv_file[column_check.name]
                    column_check.min_date = get_min(column)
                    column_check.max_date = get_max(column)

                column_check.null_values = True if column_check.name + '-null_values' in request.POST \
                    else False
                column_check.special_characters = True if column_check.name + '-special_characters' in request.POST \
                    else False

                min_max_list = [column_check.name + '-min_allowed', column_check.name + '-max_allowed',
                                column_check.name + '-min_allowed_date', column_check.name + '-max_allowed_date', ]

                for min_max in min_max_list:
                    if min_max in request.POST:
                        setattr(column_check, min_max.split(column_check.name + '-')[1],
                                float(request.POST[min_max]) if request.POST[min_max] else None)

                if column_check.name + '-allowed_values' in request.POST:
                    column_check.allowed_values = request.POST.getlist(column_check.name + '-allowed_values')

                column_check.save()

            errors = check_rows_by_column(csv_file, headers)

            return render(request, 'csv_results.html', {'errors': errors, 'filename': filename})

    return redirect(csv_upload)
