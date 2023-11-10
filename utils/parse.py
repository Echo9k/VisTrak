from datetime import datetime
from utils import process


def visitor(row):
    email = row[0]
    if not email or email == 'email':  # Skip if it's an empty email or the header
        return None

    first_visit_str = process.process_date_field(row[4])
    last_visit_str = process.process_date_field(row[5])
    # first_visit_str = first_visit_str or datetime.now()
    # last_visit_str = last_visit_str or datetime.now()
    first_visit_date = datetime.strptime(first_visit_str, "%Y-%m-%d %H:%M:%S") if first_visit_str else None

    current_year_visits = 0
    current_month_visits = 0
    if first_visit_date:
        current_year = datetime.now().year
        current_month = datetime.now().month
        current_year_visits = 1 if first_visit_date.year == current_year else 0
        current_month_visits = 1 if first_visit_date.month == current_month else 0

    return {
        'email': email,
        'fechaPrimeraVisita': first_visit_str,
        'fechaUltimaVisita': last_visit_str,
        'visitasTotales': 1,  # This should be calculated based on data
        'visitasAnioActual': current_year_visits,
        'visitasMesActual': current_month_visits
    }

    
def statistics(row):
    # Convert empty strings to None or a valid boolean representation
    bad_mail = None if row[2] == '' else row[2].lower() in ['true', '1', 'yes']
    baja = None if row[3] == '' else row[3].lower() in ['true', '1', 'yes']

    return {
        'email': row[0],
        'dynamic': row[1],  # dynamic is a placeholder for (jk, ghj, vya)
        'bad_mail': bad_mail,
        'baja': baja,
        'fecha_envio': process.process_timestamp(row[4]),
        'fecha_apertura': process.process_timestamp(row[5]) if len(row) > 5 else None,
        'opens': process.clean_integer(row[6]),
        'opens_virales': row[7] if len(row) > 7 else None,
        'fecha_click': process.process_timestamp(row[8]) if len(row) > 8 else None,
        'clicks': process.clean_integer(row[9]),
        'clicks_virales': process.clean_integer(row[10]) if len(row) > 10 else None,
        'links': process.clean_integer(row[11]),
        'ips': row[12],
        'navegadores': row[13],
        'plataformas': row[14],
    }
