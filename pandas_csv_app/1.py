import load_csv as load
import check_csv as check
import os

# CSV directory and filename
csv_dir = 'D:\\Users\\Cormac\\OneDrive\\Family\\Cormac\\College\\NUIG\\Semester 2\\Industrial Development Project\\' \
          'project_starter'
file = 'test2.csv'


def check_data(csv_file):
    csv = load.read_csv(csv_file)
    headers = load.get_headers(csv)

    print(headers)
    print(csv)

    check.check_upper(headers)

    print(load.count_records(csv))

    # Dictionary for column checks
    column_checks = {"workclass": ['Federal-gov', 'Local-gov', 'Never-worked', 'Private', 'Self-emp-inc',
                                   'Self-emp-not-inc', 'Without-pay'],
                     "marital_status": ['Never-married', 'Married-civ-spouse', 'Widowed', 'Divorced', 'Separated',
                                        'Married-spouse-absent', 'Married-AF-spouse']}

    check.check_rows(csv, headers, column_checks)
