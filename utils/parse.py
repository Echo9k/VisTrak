from datetime import datetime
from enum import Enum
from utils import process
from utils.helpers import get_row_data


class FieldIndex(Enum):
    EMAIL = 0
    DYNAMIC = 1
    BAD_MAIL = 2
    BAJA = 3
    FIRST_VISIT = 4
    LAST_VISIT = 5
    OPEN = 6
    OPEN_VIRAL = 7
    CLICK = 8
    CLICK_VIRAL = 9
    LINK = 10
    IP = 11
    BROWSER = 12
    PLATFORM = 13


def convert_to_datetime_or_none(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S") if date_str else None


def convert_to_boolean_or_none(value):
    return None if value == '' else value.lower() in ['true', '1', 'yes']


def visitor(row):
    email = get_row_data(row, FieldIndex.EMAIL)
    if not email or email == 'email':
        return None

    now = datetime.now()
    first_visit_date = convert_to_datetime_or_none(
        process.process_date_field(get_row_data(row, FieldIndex.FIRST_VISIT)))

    current_year_visits = int(first_visit_date and first_visit_date.year == now.year)
    current_month_visits = int(first_visit_date and first_visit_date.month == now.month)

    return {
        'email': email,
        'fechaPrimeraVisita': process.process_date_field(get_row_data(row, FieldIndex.FIRST_VISIT)),
        'fechaUltimaVisita': process.process_date_field(get_row_data(row, FieldIndex.LAST_VISIT)),
        'visitasTotales': 1,
        'visitasAnioActual': current_year_visits,
        'visitasMesActual': current_month_visits
    }


def statistics(row):
    return {
        'email': get_row_data(row, FieldIndex.EMAIL),
        'dynamic': get_row_data(row, FieldIndex.DYNAMIC),
        'bad_mail': convert_to_boolean_or_none(get_row_data(row, FieldIndex.BAD_MAIL)),
        'baja': convert_to_boolean_or_none(get_row_data(row, FieldIndex.BAJA)),
        'fecha_envio': process.process_timestamp(get_row_data(row, FieldIndex.FIRST_VISIT)),
        'fecha_apertura': (process.process_timestamp(get_row_data(row, FieldIndex.LAST_VISIT))
                           if len(row) > FieldIndex.LAST_VISIT.value else None),
        'opens': process.clean_integer(get_row_data(row, FieldIndex.OPEN)),
        'opens_virales': get_row_data(row, FieldIndex.OPEN_VIRAL) if len(row) > FieldIndex.OPEN_VIRAL.value else None,
        'fecha_click': (process.process_timestamp(get_row_data(row, FieldIndex.CLICK))
                        if len(row) > FieldIndex.CLICK.value else None),
        'clicks': process.clean_integer(get_row_data(row, FieldIndex.CLICK)),
        'clicks_virales': (process.clean_integer(get_row_data(row, FieldIndex.CLICK_VIRAL))
                           if len(row) > FieldIndex.CLICK_VIRAL.value else None),
        'links': process.clean_integer(get_row_data(row, FieldIndex.LINK)),
        'ips': get_row_data(row, FieldIndex.IP),
        'navegadores': get_row_data(row, FieldIndex.BROWSER),
        'plataformas': get_row_data(row, FieldIndex.PLATFORM),
    }
