# process.py
import csv
import sys
import traceback

sys.path.append(".")
from utils import loggr as loggs
from utils import (validating as validate)

def process_file(input_file_path, output_file_path):
    try:
        with open(input_file_path, 'r') as input_file, open(output_file_path, 'w', newline='') as output_file:
            reader = csv.reader(input_file)
            writer = csv.writer(output_file)
            
            # Read and write the header row
            header = next(reader)
            writer.writerow(header)
            
            for row in reader:
                if process_line(row):
                    writer.writerow(row)
    except Exception as e:
        loggs.log_error(input_file_path, e, traceback.format_exc())

def process_line(row):
    try:
        # Validate the layout of the row
        if not validate.layout(row, expected_length=15):
            loggs.log_error(row, ValueError('Layout validation failed'))
            return False

        # Validate the email format
        if row[0].lower() != 'email' and not validate.email(row[0]):
            loggs.log_error(row[0], ValueError('Invalid email format'))
            return False

        # Assume the date fields are at indices 4 (Fecha envio) and 5 (Fecha open), and index 8 (Fecha click)
        date_indices = [4, 5, 8]
        for i in date_indices:
            if row[i] != '-' and not validate.date(row[i]):
                loggs.log_error(row[i], ValueError('Invalid date format'))
                return False

        return True

    except Exception as e:
        loggs.log_error(row, e, traceback.format_exc())
        return False
