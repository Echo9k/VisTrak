from utils import loggr, parse
from psycopg2 import IntegrityError  # Import this at the top of your file


def insert_data(row, cnx):
    visitor = parse.visitor(row)
    statistics = parse.statistics(row)
    with cnx.cursor() as cursor:
        insert_visitor(visitor, cursor)
        insert_statistics(statistics, cursor)
        cnx.commit()


def insert_visitor(visitor, cursor):
    try:
        insert_query = """
        INSERT INTO visitor (email, fechaPrimeraVisita, fechaUltimaVisita, visitasTotales, visitasAnioActual, visitasMesActual)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
            fechaUltimaVisita = EXCLUDED.fechaUltimaVisita,
            visitasTotales = visitor.visitasTotales + 1,
            visitasAnioActual = EXCLUDED.visitasAnioActual,
            visitasMesActual = EXCLUDED.visitasMesActual
        """
        cursor.execute(insert_query, (
            visitor['email'],
            visitor['fechaPrimeraVisita'],
            visitor['fechaUltimaVisita'],
            visitor['visitasTotales'],
            visitor['visitasAnioActual'],
            visitor['visitasMesActual']
        ))
    except IntegrityError as e:
        loggr.error("Integrity error occurred: " + str(e))
        cnx.rollback()


def insert_statistics(statistics, cursor):
    try:
        insert_query = """
        INSERT INTO statistics (email, dynamic, bad_mail, baja, fecha_envio, fecha_apertura, opens, clicks, links, ips, navegadores, plataformas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            statistics['email'],
            statistics['dynamic'],
            statistics['bad_mail'],
            statistics['baja'],
            statistics['fecha_envio'],
            statistics['fecha_apertura'],
            statistics['opens'],
            statistics['clicks'],
            statistics['links'],
            statistics['ips'],
            statistics['navegadores'],
            statistics['plataformas']
        ))
    except IntegrityError as e:
        loggr.error("Integrity error occurred: " + str(e))
        cnx.rollback()