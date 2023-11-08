from datetime import datetime


def visitor(row):
    email = row[0]
    if not email or email == 'email':  # Skip if it's an empty email or the header
        return None

    # Initialize the variables
    first_visit_date = None
    last_visit_date = None

    # Parse dates if they are not placeholders
    if row[4] and row[4] != '-':
        try:
            first_visit_date = datetime.strptime(row[4], '%d/%m/%Y %H:%M')
        except ValueError:
            # Handle unexpected format
            print(f"Unexpected date format for first visit date: {row[4]}")

    if row[5] and row[5] != '-':
        try:
            last_visit_date = datetime.strptime(row[5], '%d/%m/%Y %H:%M')
        except ValueError:
            # Handle unexpected format
            print(f"Unexpected date format for last visit date: {row[5]}")

    # Placeholder values for visit counts
    total_visits = 1  # This should be calculated based on data
    current_year_visits = 1 if first_visit_date and first_visit_date.year == datetime.now().year else 0
    current_month_visits = 1 if first_visit_date and first_visit_date.month == datetime.now().month else 0

    return {
        'email': email,
        'fechaPrimeraVisita': first_visit_date,
        'fechaUltimaVisita': last_visit_date,
        'visitasTotales': total_visits,
        'visitasAnioActual': current_year_visits,
        'visitasMesActual': current_month_visits
    }


def date(date_str):
    if date_str and date_str != '-':
        try:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            # Handle incorrect date format
            pass
    return None


def statistics(row):
    # Extract statistics information from the row
    email = row[0]
    dynamic = row[2]  # Replace with the actual name of the field
    # ... extract other fields similarly
    fecha_envio = date(row[5])
    fecha_open = date(row[6])
    # ... extract other date fields similarly
    opens = int(row[7]) if row[7].isdigit() else 0
    opens_virales = int(row[8]) if row[8].isdigit() else 0
    # ... convert other fields to appropriate types similarly

    return {
        'email': email,
        'dynamic': dynamic,
        # ... include other fields similarly
        'Fecha envio': fecha_envio,
        'Fecha open': fecha_open,
        'Opens': opens,
        'Opens virales': opens_virales,
        # ... include other fields similarly
    }
