import re
import math
from .load_csv import get_headers
from .models import ColumnCheck
from django.forms.models import model_to_dict

errors = {}


def check_upper_headers(array):  # Check if any letter is upper case and print
    global errors
    chk = False
    for word in array:
        if not word.islower():
            if chk is False:
                errors['Headers'] = []

            errors['Headers'].append(
                'Uppercase letter found: ' + word + ' (Column: ' + str(array.index(word) + 1) + ')')
            chk = True

    return chk


def check_null_values_orig(array):  # Check all values are present and that no rows are too long
    if array.isna().values.any():  # Return true if any null values are found
        return True


def check_null_values(value):  # Check all values are present and that no rows are too long (for tuples)
    if isinstance(value, float):  # Only floats can be NaN
        if math.isnan(value):  # Return true if any null values are found
            return 'Null value '
        else:
            return False


def check_characters_against_regex(value, regex_string):  # Check for special characters
    if isinstance(value, str):  # Don't see need to check non-string values as they won't contain special values
        for letter in value:
            if re.search(regex_string, letter) is None:
                return 'Special character '
        else:
            return False


def check_special_characters(value):
    return check_characters_against_regex(value, '[a-zA-ZÀ-ÿ0-9-_<>=]')


def check_against_array(value, array):  # Check if value exists in array
    if value in array:
        return True
    else:
        return value


def append_row_number_to_dict(row):  # Appends row number to dictionary
    global errors
    if (row.Index + 2) not in errors:  # Check if row has been added
        errors[(row.Index + 2)] = []


def check_rows(csv_file, checks):
    global errors
    errors = {}
    headers = get_headers(csv_file)

    if 'headers' in checks:
        check_upper_headers(headers)
        checks.remove('headers')

    for row in csv_file.itertuples():  # Iterate over rows as named tuples
        for i, value in enumerate(row):  # enumerate for printing out header later
            for check in checks:
                chk = globals()['check_' + check](value)
                if not (chk is None or chk is False):
                    append_row_number_to_dict(row)
                    errors[(row.Index + 2)].append(str(chk) + 'found in column ' + headers[i - 1])

    return errors


def check_rows_by_column(csv_file, column_checks):
    global errors
    errors = {}

    headers = get_headers(csv_file)

    for row in csv_file.itertuples():
        for check in column_checks:
            chk = check_against_array(row[headers.index(check.name) + 1], check.allowed_values)
            if chk is not True:  # If check_against_array flags an invalid value
                append_row_number_to_dict(row)
                errors[(row.Index + 2)].append('Invalid value found in column ' + check.name + ': ' + str(chk))


# def check
