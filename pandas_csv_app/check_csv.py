import re
import math


def check_upper(array):  # Check if any letter is upper case and print
    chk = False
    for word in array:
        if not word.islower():
            print('Uppercase letter found: ' + word + ' (Column: ' + str(array.index(word) + 1) + ')')
            chk = True

    return chk


def check_null_values(array):        # Check all values are present and that no rows are too long
    if array.isna().values.any():    # Return true if any null values are found
        return True


def check_null_values_tuples(value):    # Check all values are present and that no rows are too long (for tuples)
    if isinstance(value, float):        # Only floats can be NaN
        if math.isnan(value):           # Return true if any null values are found
            return True
        else:
            return False


def check_characters_against_string(value, regex_string):  # Check for special characters
    if isinstance(value, str):  # Don't see need to check non-string values as they won't contain special values
        for letter in value:
            if re.search(regex_string, letter) is None:
                return True


def check_against_array(value, array):                  # Check if value exists in array
    if value in array:
        return True
    else:
        return value


def check_value_null_and_characters(value):  # Could pass regex here obviously if so desired
    null_value = check_null_values_tuples(value)
    if null_value:
        return 'Null value '
    elif null_value is None:  # check_null_values_tuples returns False if it's a float that isn't NaN
        if check_characters_against_string(value, '[a-zA-ZÀ-ÿ0-9-_<>=]'):  # Include accented characters
            return 'Special character '


def print_row_number(row, row_error):  # Prints row number
    if not row_error:                  # Check if row number has been printed
        print(str(row.Index + 2) + ": ")
        row_error = True

    return row_error


def check_rows(csv_file, headers, column_checks):
    for row in csv_file.itertuples():       # Iterate over rows as named tuples
        row_error = False                   # Variable to ensure row number is only printed once
        for i, value in enumerate(row):     # enumerate for printing out header later
            chk = check_value_null_and_characters(value)        # Check value
            if chk is not None:
                row_error = print_row_number(row, row_error)
                print(str(chk) + 'found in column ' + headers[i - 1])

        for key in column_checks:
            chk = check_against_array(row[headers.index(key) + 1], column_checks[key])
            if chk is not True:             # If check_against_array flags an invalid value
                if check_value_null_and_characters(row[headers.index(key) + 1]) is None:  # No need to print otherwise
                    row_error = print_row_number(row, row_error)
                    print('Invalid value found in column ' + key + ': ' + str(chk))
