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
            row_data = ','.join(map(str, row)) if row is not None else 'Row was None'
            cursor.execute(error_insert, (
                filename,
                row_data,
                error_message,
                error_type,
                error_code,
                stack_trace
            ))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            print(f"Error logging failed: {error_type, e, row}")
            cnx.rollback()
