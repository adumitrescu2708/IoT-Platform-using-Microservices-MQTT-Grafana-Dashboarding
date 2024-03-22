'''
    Copyright: Dumitrescu Alexandra - Jan 2024
'''
from influxdb import InfluxDBClient
import datetime

# constant values used for connection to the InfluxDB database
DATABASE_URL        = "sprc3_influx-db-service"
DATABASE_PORT       = 8086
DATABASE_NAME       = "IoTSPRC"
MEASUREMENT_NAME    = 'IoT'

# connect to the influx db client
db_client = InfluxDBClient(DATABASE_URL, DATABASE_PORT, database=DATABASE_NAME)

# switch to the corresponding database
db_client.switch_database(DATABASE_NAME)  

# we create a measurement for all received info and add tags in order to identify correctly the data
def parse_entry_database(location : str, station : str, key : str, value : float, measure_date : datetime):
    # metric is station/key, used in the UPB Iot Dashboard
    metric = str(station + "." + key)
    
    # add to the measurement
    data = {
        'measurement': MEASUREMENT_NAME,
        
        # send the location, the station, the metric and the key as tags
        'tags': {
            'location': location,
            'station': station,
            'measure': key,
            'metric' : metric
        },
        
        # format the date
        'time': measure_date.strftime("%Y-%m-%d %H:%M:%S"),
        
        # set the value
        'fields': {
            'value': value
        }
    }
    
    return data

# add a list of entries to the database
def add_entries_database(entries) -> None:
    db_client.write_points(entries)