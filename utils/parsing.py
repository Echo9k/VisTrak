from datetime import datetime


# Define transformation functions (complete these based on your business logic)
def visitor(row):
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


def statistics(row):
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
