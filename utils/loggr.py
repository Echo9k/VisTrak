import os
import sys
sys.path.append(os.path.join(os.getcwd()))

import os
import logging
from utils.helpers import get_conf_info, read_config_file


def cnx_error(filename, cnx, row, error, stack_trace):
    error_message = str(error)
    error_type = type(error).__name__
    with cnx.cursor() as cursor:
        error_insert = """
        INSERT INTO errors (filename, row_data, error_message, error_type, error_code, stack_trace, error_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        row_data = 'Row was None' if row is None else ','.join(map(str, row))
        try:
            cursor.execute(error_insert, (
                filename,
                row_data,
                error_message,
                error_type,
                error_type,
                stack_trace
            ))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            logging.error("Error logging failed: %s, %s, %s", error_type, e, row)


class Logger:
    def __init__(self, log_key, level=logging.INFO, config_file='./config/config.conf'):
        self.config = read_config_file(config_file)
        log_file_path = os.getenv('BASE_DIR') + get_conf_info(self.config, log_key=log_key)
        self.setup_logger(log_file_path, level)

    def setup_logger(self, log_file_path, level):
        try:
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        except PermissionError as e:
            # log to console if we can't write to the log file
            
            print(f">>> Permission error creating log file: {log_file_path}")
            raise(e)
        else:
            logging.basicConfig(filename=log_file_path, level=level, format='%(asctime)s - %(levelname)s - %(message)s')

    @staticmethod
    def log_error(data, exception, traceback_info):
        logging.error("Data: %s, Exception: %s, Traceback: %s", data, exception, traceback_info)