import psycopg2


def cnx_error(row, error, error_type, error_code, stack_trace, cnx):
    with cnx.cursor() as cursor:
        error_insert = """
        INSERT INTO errors (filename, row_data, error_message, error_detail, error_type, error_code, stack_trace, error_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
        """
        try:
            cursor.execute(error_insert, (
                row.get('filename'),       # Assuming 'filename' is part of the row dictionary
                ','.join(map(str, row)),   # Join the row data into a string
                str(error),                # Convert error to string
                error_detail,              # Detailed error message
                error_type,                # Type of error
                error_code,                # Error code
                stack_trace                # Stack trace information
            ))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            # If logging fails, consider logging this to a file or print to the console
            print(f"Error logging failed: {e}")
            cnx.rollback()