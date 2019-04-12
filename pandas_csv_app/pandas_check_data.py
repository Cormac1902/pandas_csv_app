from .load_csv import read_csv_file, get_headers, count_records
from .check_csv import check_upper, check_rows
# import os

# CSV directory and filename
csv_dir = 'D:\\Users\\Cormac\\OneDrive\\Family\\Cormac\\College\\NUIG\\Semester 2\\Industrial Development Project\\' \
          'project_starter'
file = 'test2.csv'


def check_data(csv_file):
    csv = read_csv_file(csv_file)
    headers = get_headers(csv)

    check_upper(headers)

    # Dictionary for column checks
    column_checks = {"workclass": ['Federal-gov', 'Local-gov', 'Never-worked', 'Private', 'Self-emp-inc',
                                   'Self-emp-not-inc', 'Without-pay'],
                     "marital_status": ['Never-married', 'Married-civ-spouse', 'Widowed', 'Divorced', 'Separated',
                                        'Married-spouse-absent', 'Married-AF-spouse']}

    return check_rows(csv, headers, column_checks)
