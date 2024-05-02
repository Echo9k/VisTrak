# logging.py
import logging
import configparser
import psycopg2


# Configure logging at the start
config = configparser.ConfigParser()
config.read('./config/config.conf')
logging.basicConfig(filename=config['path']['log'], level=config['log']['log.level'])


def log_error(data, exception, traceback_info):
    """
    Logs an error message with provided data, exception, and traceback information.

    Args:
        data: Data associated with the error.
        exception: The exception that occurred.
        traceback_info: Information about the traceback.

    Returns:
        None
    """
    # Use lazy formatting for logging
    logging.error("Data: %s, Exception: %s, Traceback: %s", data, exception, traceback_info)


def cnx_error(filename, cnx, row, error, stack_trace):
    """
    Handles database errors by inserting error details into a database table.

    Args:
        filename: The name of the file where the error occurred.
        cnx: Database connection object.
        row: Data associated with the error.
        error: The error object.
        stack_trace: Stack trace information.

    Returns:
        None
    """
    error_message = str(error)
    error_type = type(error).__name__

    with cnx.cursor() as cursor:
        error_insert = """
        INSERT INTO errors (filename, row_data, error_message, error_type, error_code, stack_trace, error_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        try:
            # Streamline row data handling
            row_data = 'Row was None' if row is None else ','.join(map(str, row))
            cursor.execute(error_insert, (
                filename,
                row_data,
                error_message,
                error_type,
                error_type,  # Use error_type for both error_type and error_code
                stack_trace
            ))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            # Use lazy formatting for logging
            logging.error("Error logging failed: %s, %s, %s", error_type, e, row)
