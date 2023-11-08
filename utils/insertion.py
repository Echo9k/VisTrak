from utils import (validation as validate,
                   parsing as parse,
                   logging)

        
def insert_data(row, cnx):
    visitor = parse.visitor(row)
    statistics = parse.statistics(row)
    with cnx.cursor() as cursor:
        insert_visitor(visitor, cursor)
        insert_statistics(statistics, cursor)
        cnx.commit()


def insert_visitor(visitor, cursor):
    visitor_insert = """
    INSERT INTO visitor (email, fechaPrimeraVisita, fechaUltimaVisita, visitasTotales, visitasAnioActual, visitasMesActual)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(visitor_insert,(
        visitor['email'],
        visitor['fechaPrimeraVisita'],
        visitor['fechaUltimaVisita'],
        visitor['visitasTotales'],
        visitor['visitasAnioActual'],
        visitor['visitasMesActual']
        )
    )


def insert_statistics(statistics, cursor):
    statistics_insert = """
    INSERT INTO statistics (email, jyv, Badmail, Baja, Fecha_envio, Fecha_open, Opens, Opens_virales, Fecha_click, Clicks, Clicks_virales, Links, IPs, Navegadores, Plataformas)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(statistics_insert, (
        statistics['email'],
        statistics['dynamic'],
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
    )
)