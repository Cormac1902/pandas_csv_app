from pandas import read_csv

# https://towardsdatascience.com/data-cleaning-with-python-and-pandas-detecting-missing-values-3e9c6ebcf78b
missing_values = ["N/A", "N/a", "n/A", "n/a", "Na", "nA","na", "---", "--", "-", " ", "?"]


def read_csv_file(csv_file):  # Read CSV file
    return read_csv(csv_file, na_values=missing_values)


def get_headers(csv_file):  # Obtain headers from CSV file
    return csv_file.columns.tolist()


def count_records(csv_file):                 # Count records in file
    return len(csv_file)
