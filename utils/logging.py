# Define error logging function
def log_error(row, error):
    with cnx.cursor() as cursor:
        error_insert = """
        INSERT INTO errors (error_detail, error_row)
        VALUES (%s, %s)
        """
        try:
            cursor.execute(error_insert, (error, ','.join(row)))
            cnx.commit()
        except psycopg2.DatabaseError as e:
            # If logging fails, you might want to log this to a file or print to the console
            print(f"Error logging failed: {e}")
            cnx.rollback()