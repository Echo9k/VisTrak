import os
import datetime
import psycopg2
import configparser

# Load config file
config = configparser.ConfigParser()
config.read('/workspaces/anaconda-postgres/config/config.conf')
source = config['source']

# Connect to Postgres database
cnx = psycopg2.connect(
    database=source['database'],
    user=source['user'],
    password=source['password'],
    host=source.get('host', 'localhost'),  # Use 'localhost' as default if not set
    port=source.get('port', '5432')  # Use '5432' as default if not set
)
cursor = cnx.cursor()


# Process each file in temp directory
for filename in os.listdir('/workspaces/anaconda-postgres/data/temp'):
    if filename.endswith('.csv'):
        with open(os.path.join('/workspaces/anaconda-postgres/data/temp', filename), 'r') as f:
            for line in f:
                row = line.strip().split(',')
                if validate_layout(row):
                    if validate_email(row[0]) and validate_date(row[1]):
                        visitor = parse_visitor({'email': row[0], 'date': row[1]})
                        statistics = parse_statistics({'email': row[0], 'jyv': row[2], 'Badmail': row[3], 'Baja': row[4], 'Fecha envio': row[5], 'Fecha open': row[6], 'Opens': row[7], 'Opens virales': row[8], 'Fecha click': row[9], 'Clicks': row[10], 'Clicks virales': row[11], 'Links': row[12], 'IPs': row[13], 'Navegadores': row[14], 'Plataformas': row[15]})
                        try:
                            # Insert visitor and statistics into Postgres tables
                            visitor_insert = "INSERT INTO visitor (email, fechaPrimeraVisita, fechaUltimaVisita, visitasTotales, visitasAnioActual, visitasMesActual) VALUES (%s, %s, %s, %s, %s, %s)"
                            cursor.execute(visitor_insert, (visitor['email'], visitor['fechaPrimeraVisita'], visitor['fechaUltimaVisita'], visitor['visitasTotales'], visitor['visitasAnioActual'], visitor['visitasMesActual']))
                            statistics_insert = "INSERT INTO statistics (email, jyv, Badmail, Baja, Fecha_envio, Fecha_open, Opens, Opens_virales, Fecha_click, Clicks, Clicks_virales, Links, IPs, Navegadores, Plataformas) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cursor.execute(statistics_insert, (statistics['email'], statistics['jyv'], statistics['Badmail'], statistics['Baja'], statistics['Fecha envio'], statistics['Fecha open'], statistics['Opens'], statistics['Opens virales'], statistics['Fecha click'], statistics['Clicks'], statistics['Clicks virales'], statistics['Links'], statistics['IPs'], statistics['Navegadores'], statistics['Plataformas']))
                            cnx.commit()
                        except Exception as e:
                            # Log error if insert fails
                            log_error(row, str(e))
                    else:
                        # Log error if email or date is invalid
                        log_error(row, 'Invalid email or date')
        # Delete file once processed
        os.remove(os.path.join('/workspaces/anaconda-postgres/data/temp', filename))

# Close Postgres connection
cursor.close()
cnx.close()
