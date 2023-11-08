import json
import psycopg2
import configparser

# Load config file
config = configparser.ConfigParser()
config.read('../config/config.conf')
configs = config['source']


# Load configuration file (json format) for source database 
with open(configs['config_file']) as json_file:
    source = json.load(json_file)

# Establish connection to the PostgreSQL database
try:
    cnx = psycopg2.connect(
        database=source['database'],
        user=source['user'],
        password=source['password'],
        host=source.get('db.host', 'localhost'),  # Use 'localhost' as default if 'db.host' is not set
        port=source.get('db.port', '5432')  # Use '5432' as default if 'db.port' is not set
    )
    cursor = cnx.cursor()

    # Test query to ensure connection is established
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record, "\n")

except Exception as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # Close the cursor and connection
    if (cnx):
        cursor.close()
        cnx.close()
        print("PostgreSQL connection is closed")