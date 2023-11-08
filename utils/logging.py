import psycopg2


def cnx_error(filename, cnx, row, error, stack_trace):
    error_message = str(error)
    error_type = type(error).__name__
    error_code = error.__class__.__name__

    with cnx.cursor() as cursor:
        error_insert = """
        INSERT INTO errors (filename, row_data, error_message, error_type, error_code, stack_trace, error_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        try:
            cursor.execute(error_insert, (
                filename,                  # Pass the filename
                ','.join(map(str, row)),   # Join the row data into a string
                error_message,             # Convert error to string
                error_type,                # Type of error
                error_code,                # Error code
                stack_trace                # Stack trace information
            ))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            # If logging fails, consider logging this to a file or print to the console
            print(f"Error logging failed: {e}")
            cnx.rollback()

