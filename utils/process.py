# process.py

import traceback
from datetime import datetime
from utils import loggr as loggs, insert, validate


def process_file(filename, cnx):
    """
    Processes a file by skipping the header row and processing each line.

    Args:
        filename (str): The path to the file to be processed.
        cnx: The connection to the database.

    Returns:
        None
    """
    with open(filename, 'r') as f:
        next(f)  # Skip the header row
        for line in f:
            process_line(filename=filename, cnx=cnx, line=line)


def process_timestamp(timestamp_str, format='iso', return_type='str'):
    """
    Processes a timestamp string, converting it to a datetime object or a formatted string.

    Args:
        timestamp_str (str): The timestamp string to process.
        format (str): The format to return the timestamp in (default is 'iso').
        return_type (str): The type of the return value (default is 'str').

    Returns:
        datetime object or formatted string, or None if the input is not a valid timestamp.
    """
    try:
        dt = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M")
        if return_type == 'datetime':
            return dt
        return dt.strftime("%Y-%m-%d %H:%M:%S") if format == 'iso' else dt.strftime(format)
    except ValueError:
        return None


def process_date_field(date_str):
    """
    Processes a date string, returning it in ISO format if valid, or None otherwise.

    Args:
        date_str (str): The date string to process.

    Returns:
        ISO formatted date string or None.
    """
    if validate.date(date_str) and date_str != '-':
        if date_obj := process_timestamp(date_str, return_type='datetime'):
            return date_obj.strftime("%Y-%m-%d %H:%M:%S")
    return None


def clean_integer(value):
    """
    Cleans an input value by converting it to an integer.

    Args:
        value: The value to clean.

    Returns:
        int or None if the value is not a valid integer.
    """
    try:
        return int(value)
    except ValueError:
        return None


def process_line(filename, cnx, line):
    """
    Processes a line from a file, validating its layout, email format, and date fields.

    Args:
        filename (str): The name of the file being processed.
        cnx: The database connection.
        line (str): The line to process.

    Returns:
        None
    """
    row = line.strip().split(',')
    err_value = row
    try:
        if not validate.layout(row, expected_length=15):
            print(f"Validation failed: Layout validation failed for row {err_value}")
            raise ValueError('Layout validation failed')
        if row[0].lower() != 'email' and not validate.email(row[0]):
            print(f"Validation failed: Invalid email format for '{err_value[0]}'")
            raise ValueError('Invalid email format')
        date_indices = [4, 5, 8]
        for i in date_indices:
            if row[i] != '-' and not validate.date(row[i]):
                print(f"Validation failed: Invalid date format for '{row[i]}' at position {i}")
                raise ValueError('Invalid date format')
        insert.insert_data(row, cnx)
    except Exception as e:
        loggs.cnx_error(filename, cnx, err_value, e, traceback.format_exc())
