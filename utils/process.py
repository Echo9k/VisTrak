import traceback
from datetime import datetime
from utils import (logging, insertion,
                   validation as validate)
from psycopg2.errors import UniqueViolation
        

from utils import (parsing as parse,
                   logging, insertion)


def process_file(filename, cnx):
    header_skipped = False
    with open(filename, 'r') as f:
        for line in f:
            if not header_skipped:  # Skip the header row
                header_skipped = True
                continue
            process_line(filename=filename, cnx=cnx, line=line)  # Now we process the line assuming the header is already skipped


def process_line(filename, cnx, line):
    row = line.strip().split(',')
    err_value = row  # Initialize to track the value causing an error
    try:
        # Validate the layout of the row
        if not validate.layout(row, expected_length=15):
            err_value = row
            print(f"Validation failed: Layout validation failed for row {err_value}")
            raise ValueError('Layout validation failed')

        # Validate the email format
        if row[0].lower() != 'email' and not validate.email(row[0]):
            err_value = row[0]
            print(f"Validation failed: Invalid email format for '{err_value}'")
            raise ValueError('Invalid email format')

        # Assume the date fields are at indices 4 (Fecha envio) and 5 (Fecha open), and index 8 (Fecha click)
        date_indices = [4, 5, 8]
        for i in date_indices:
            if row[i] != '-' and not validate.date(row[i]):
                err_value = row[i]
                print(f"Validation failed: Invalid date format for '{err_value}' at position {i}")
                raise ValueError('Invalid date format')

        # If all validations pass
        insertion.insert_data(row, cnx)
    # except UniqueViolation:
    #     cnx.rollback()
    except Exception as e:
        logging.cnx_error(filename, cnx, err_value, e, traceback.format_exc())


def process_timestamp(timestamp_str, format='iso', return_type='str'):
    """
    Converts a timestamp string to a datetime object or a string in the specified format.
    If the input is not a valid timestamp, it returns None.
    """
    try:# Convert to a datetime object
        dt = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M")
        
        # Return datetime object if return_string is False
        if return_type == 'datetime':
            return dt
        
        # Return string in the specified format
        if format == 'iso':
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dt.strftime(format)
        
    except ValueError:
        # If there is a ValueError, it means the string was not in the expected format
        return None


def format_datetime(dt, format='iso'):
    if format == 'iso':
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return dt.strftime(format)


def process_date_field(date_str):
    """
    Process a date string, returning it in ISO format if valid, or None otherwise.
    """
    if validate.date(date_str) and date_str != '-':
        date_obj = process_timestamp(date_str, return_type='datetime')
        if date_obj:
            return format_datetime(date_obj, format='iso')
    return None


def clean_integer(value):
    try:
        return int(value)
    except ValueError:
        # Return None if the value is not a valid integer
        return None


def process_line(filename, cnx, line):
    row = line.strip().split(',')
    err_value = row  # Initialize to track the value causing an error
    try:
        # Validate the layout of the row
        if not validate.layout(row, expected_length=15):
            err_value = row
            print(f"Validation failed: Layout validation failed for row {err_value}")
            raise ValueError('Layout validation failed')

        # Validate the email format
        if row[0].lower() != 'email' and not validate.email(row[0]):
            err_value = row[0]
            print(f"Validation failed: Invalid email format for '{err_value}'")
            raise ValueError('Invalid email format')

        # Assume the date fields are at indices 4 (Fecha envio) and 5 (Fecha open), and index 8 (Fecha click)
        date_indices = [4, 5, 8]
        for i in date_indices:
            if row[i] != '-' and not validate.date(row[i]):
                err_value = row[i]
                print(f"Validation failed: Invalid date format for '{err_value}' at position {i}")
                raise ValueError('Invalid date format')

        # If all validations pass
        insertion.insert_data(row, cnx)
    # except UniqueViolation:
    #     cnx.rollback()
    except Exception as e:
        logging.cnx_error(filename, cnx, err_value, e, traceback.format_exc())


def process_timestamp(timestamp_str, format='iso', return_type='str'):
    """
    Converts a timestamp string to a datetime object or a string in the specified format.
    If the input is not a valid timestamp, it returns None.
    """
    try:# Convert to a datetime object
        dt = datetime.strptime(timestamp_str, "%d/%m/%Y %H:%M")
        
        # Return datetime object if return_string is False
        if return_type == 'datetime':
            return dt
        
        # Return string in the specified format
        if format == 'iso':
            return dt.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return dt.strftime(format)
        
    except ValueError:
        # If there is a ValueError, it means the string was not in the expected format
        return None

def format_datetime(dt, format='iso'):
    if format == 'iso':
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    else:
        return dt.strftime(format)


def process_date_field(date_str):
    """
    Process a date string, returning it in ISO format if valid, or None otherwise.
    """
    if validate.date(date_str) and date_str != '-':
        date_obj = process_timestamp(date_str, return_type='datetime')
        if date_obj:
            return format_datetime(date_obj, format='iso')
    return None


def clean_integer(value):
    try:
        return int(value)
    except ValueError:
        # Return None if the value is not a valid integer
        return None
