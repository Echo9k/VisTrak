import os
import datetime
import psycopg2
import configparser
import re

# Load config file
config = configparser.ConfigParser()
config.read('/workspaces/anaconda-postgres/config/config.conf')
source = config['source']

# Connect to Postgres database
cnx = psycopg2.connect(
    database=source['database'],
    user=source['user'],
    password=source['password']
)

# Define validation functions
def validate_layout(row):
    expected_columns = 16  # Update the number based on your file structure
    return len(row) == expected_columns


def validate_email(email):
    # Simple regex for email validation
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None


def validate_date(date_str):
    try:
        # Assuming the date format is 'YYYY-MM-DD HH:MM:SS'
        datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False


# Define transformation functions (complete these based on your business logic)
def parse_visitor(row):
    # Extract visitor information from the row
    email = row[0]
    first_visit_date = datetime.datetime.strptime(row[1], '%Y-%m-%d')
    last_visit_date = datetime.datetime.strptime(row[1], '%Y-%m-%d')
    # You might want to adjust the logic below based on how you calculate total visits
    total_visits = 1  # Placeholder, you would need to calculate this based on previous data
    current_year_visits = 1 if first_visit_date.year == datetime.datetime.now().year else 0
    current_month_visits = 1 if first_visit_date.month == datetime.datetime.now().month else 0

    return {
        'email': email,
        'fechaPrimeraVisita': first_visit_date,
        'fechaUltimaVisita': last_visit_date,
        'visitasTotales': total_visits,
        'visitasAnioActual': current_year_visits,
        'visitasMesActual': current_month_visits
    }


def parse_statistics(row):
    # Extract statistics information from the row
    email = row[0]
    jyv = row[2]
    # ... extract other fields similarly
    fecha_envio = datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S')
    fecha_open = datetime.datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')
    # ... extract other date fields similarly
    opens = int(row[7])  # Assuming these fields are integer counts
    opens_virales = int(row[8])
    # ... convert other fields to appropriate types similarly

    return {
        'email': email,
        'jyv': jyv,
        # ... include other fields similarly
        'Fecha envio': fecha_envio,
        'Fecha open': fecha_open,
        'Opens': opens,
        'Opens virales': opens_virales,
        # ... include other fields similarly
    }


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

# Process each file in temp directory
temp_dir = config['source']['temp_dir']
for filename in os.listdir(temp_dir):
    if filename.endswith('.csv'):
        with open(os.path.join(temp_dir, filename), 'r') as f:
            for line in f:
                row = line.strip().split(',')
                if validate_layout(row):
                    if validate_email(row[0]) and validate_date(row[5]) and validate_date(row[6]) and validate_date(row[9]):
                        visitor = parse_visitor(row)
                        statistics = parse_statistics(row)
                        try:
                            with cnx.cursor() as cursor:
                                visitor_insert = """
                                INSERT INTO visitor (email, fechaPrimeraVisita, fechaUltimaVisita, visitasTotales, visitasAnioActual, visitasMesActual)
                                VALUES (%s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(visitor_insert, (
                                    visitor['email'],
                                    visitor['fechaPrimeraVisita'],
                                    visitor['fechaUltimaVisita'],
                                    visitor['visitasTotales'],
                                    visitor['visitasAnioActual'],
                                    visitor['visitasMesActual']
                                ))
                                
                                statistics_insert = """
                                INSERT INTO statistics (email, jyv, Badmail, Baja, Fecha_envio, Fecha_open, Opens, Opens_virales, Fecha_click, Clicks, Clicks_virales, Links, IPs, Navegadores, Plataformas)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """
                                cursor.execute(statistics_insert, (
                                    statistics['email'],
                                    statistics['jyv'],
                                    statistics['Badmail'],
                                    statistics['Baja'],
                                    statistics['Fecha envio'],
                                    statistics['Fecha open'],
                                    statistics['Opens'],
                                    statistics['Opens virales'],
                                    statistics['Fecha click'],
                                    statistics['Clicks'],
                                    statistics['Clicks virales'],
                                    statistics['Links'],
                                    statistics['IPs'],
                                    statistics['Navegadores'],
                                    statistics['Plataformas']
                                ))
                                cnx.commit()
                        except psycopg2.DatabaseError as e:
                            log_error(row, str(e))
                            cnx.rollback()
                    else:
                        log_error(row, 'Invalid email or date')
        # Delete file once processed
        os.remove(os.path.join(temp_dir, filename))

# Close Postgres connection
cnx.close()
