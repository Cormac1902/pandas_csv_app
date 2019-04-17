from pandas import read_csv
from pandas.io.common import EmptyDataError


# https://towardsdatascience.com/data-cleaning-with-python-and-pandas-detecting-missing-values-3e9c6ebcf78b
# Read CSV file
def read_csv_file(csv_file, missing_values):
    try:
        if missing_values:
            return read_csv(csv_file, na_values=missing_values)
        else:
            return read_csv(csv_file,
                            na_values=["N/A", "N/a", "n/A", "n/a", "Na", "nA", "na", "---", "--", "-", " ", "?"])
    except EmptyDataError:
        return False


def get_headers(csv_file):  # Obtain headers from CSV file
    return csv_file.columns.tolist()


def get_data_types(csv_file):  # Obtain column data types
    return csv_file.dtypes


def count_records(csv_file, column=None):  # Count records in file
    if column is None:
        return len(csv_file)
    else:
        return csv_file[column].count()


def count_unique_values(column):
    return column.nunique()


def get_unique_values(column):
    return sorted(column.unique())


def get_min(column):
    return column.min()


def get_max(column):
    return column.max()
