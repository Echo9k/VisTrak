import os
import datetime
import psycopg2
import configparser
import re

from utils import (validation as validate,
                   parsing as parse,
                   logging)

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



# Process each file in temp directory
temp_dir = config['source']['temp_dir']
for filename in os.listdir(temp_dir):
    if filename.endswith('.csv'):
        with open(os.path.join(temp_dir, filename), 'r') as f:
            for line in f:
                row = line.strip().split(',')
                if validate.layout(row):
                    if validate.email(row[0]) and validate.date(row[5]) and validate.date(row[6]) and validate.date(row[9]):
                        visitor = parse.visitor(row)
                        statistics = parse.statistics(row)
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
                            logging.log_error(row, str(e))
                            cnx.rollback()
                    else:
                        logging.log_error(row, 'Invalid email or date')
        # Delete file once processed
        os.remove(os.path.join(temp_dir, filename))

# Close Postgres connection
cnx.close()
