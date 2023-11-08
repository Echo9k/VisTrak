import traceback
from utils import validation as validate, parsing as parse, logging


def file(filename, cnx):
    header_skipped = False
    with open(filename, 'r') as f:
        for line in f:
            if not header_skipped:  # Skip the header row
                header_skipped = True
                continue
            line(line, cnx)  # Now we process the line assuming the header is already skipped


def line(line, cnx):
    row = line.strip().split(',')
    err_value = None  # Initialize to track the value causing an error
    try:
        if not validate.layout(row):
            err_value = row
            print(f"Validation failed: Layout validation failed for row {err_value}")
            raise ValueError('Layout validation failed')

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
        insert_data(row, cnx)
    except Exception as e:
        err_val = err_value or row
        print(f"Exception occurred: {e}."
            f"Traceback: {traceback.format_exc()}"
            f"Error value: {err_value}")
        logging.cnx_error(filename, cnx, err_value, e, traceback.format_exc())