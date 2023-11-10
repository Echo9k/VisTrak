from utils import loggr, parse


def insert_data(row, cnx):
    visitor = parse.visitor(row)
    statistics = parse.statistics(row)
    with cnx.cursor() as cursor:
        insert_visitor(visitor, cursor)
        insert_statistics(statistics, cursor)
        cnx.commit()


from psycopg2 import IntegrityError  # Import this at the top of your file

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
        loggs.error("Integrity error occurred: " + str(e))
        # Handle the unique violation error
        cnx.rollback()



from psycopg2 import IntegrityError  # Import this at the top of your file

def insert_statistics(statistics, cursor):
    try:
        insert_query = """
        INSERT INTO statistics (email, dynamic, bad_mail, baja, fecha_envio, fecha_apertura, opens, clicks, links, ips, navegadores, plataformas)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (email) DO UPDATE SET
            dynamic = EXCLUDED.dynamic,
            bad_mail = EXCLUDED.bad_mail,
            baja = EXCLUDED.baja,
            fecha_envio = EXCLUDED.fecha_envio,
            fecha_apertura = EXCLUDED.fecha_apertura,
            opens = EXCLUDED.opens,
            clicks = EXCLUDED.clicks,
            links = EXCLUDED.links,
            ips = EXCLUDED.ips,
            navegadores = EXCLUDED.navegadores,
            plataformas = EXCLUDED.plataformas
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
        loggs.error("Integrity error occurred: " + str(e))
        # Handle the unique violation error
        cnx.rollback()


