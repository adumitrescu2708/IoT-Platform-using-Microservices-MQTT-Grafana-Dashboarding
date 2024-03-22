'''
    Copyright: Dumitrescu Alexandra - Jan 2024
'''
import paho.mqtt.client as mqtt
import os, time, logging, json, datetime
import parser
from database import db_client
import database

# broker url
BROKER_URL = "sprc3_mosquitto-broker-service"

# debug flag - active if the DEBUG_DATA_FLOW env variable is set - in this case, the logging messages are printed
debug = True if os.environ.get("DEBUG_DATA_FLOW") == "true" else False

# client id
CLIENT_ID = "admin"

# create the logger
logger = logging.getLogger()


def on_message(client, userdata, msg):
    # check the topic format restriction of "location/station"
    if not parser.check_topic_format(msg.topic):
        return
    
    # check if the received payload is a json
    if not parser.check_json_payload(msg.payload.decode()):
        return
    
    # print the received topic if the debug flag is active
    if debug:
        logger.info(f"Received a message by topic [`{msg.topic}`]")

    # load the received payload
    payload = json.loads(msg.payload.decode())
    
    # get the timestamp in Date format
    measure_date = None 
    
    # if the "timestamp" field is not given in the JSON payload, set the timestamp to NOW
    if not "timestamp" in payload:
        measure_date = datetime.datetime.now()
        
        # print log if the debug flag is active
        if debug:
            logger.info("Data timestamp is NOW")
    else:
        # if the timestamp is specified try convert to the restricted format
        try:
            measure_date = datetime.datetime.strptime(payload["timestamp"], "%Y-%m-%dT%H:%M:%S%z")
            if debug: 
                logger.info(f"Data timestamp is {measure_date}")
        except:
            # if the given timestamp does not follow the restriction, set to current datetime
            measure_date = datetime.datetime.now()
            if debug: 
                logger.info("Data timestamp is NOW")
        
    # extract the location and the station from the JSON payload
    location    = msg.topic.split('/')[0]
    station     = msg.topic.split('/')[1] 
    entries     = []

    # for every pair of key-value in the JSON payload
    for key, value in payload.items():
        
        # check if the value is float or int
        if not parser.check_entry_format(key, value):
            continue
        
        # compute the time series - location/station/metric
        time_series = msg.topic.replace('/', '.') + "." + str(key)  
        
        # print info if the debug flag is active
        if debug:
            logger.info(time_series + " " + str(value))
        
        # add the entry in the list of entries
        entries.append(database.parse_entry_database(location, station, key, float(value), measure_date))
    
    # add the list of entries to the database
    database.add_entries_database(entries)
    
    # mark the end of a message
    if debug: 
        logger.info("")     


def setup_logger(logger):
    # create a stream handler and set the level to INFO in avoid printing all debug messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    
    # set the time format
    formatter = logging.Formatter('%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(formatter)
    logger.setLevel(logging.INFO)
    logger.addHandler(ch)


def setup_MQTT_client():
    # create the MQTT client and connect to the broker
    mqtt_client = mqtt.Client(CLIENT_ID)
    
    # set the on_message function
    mqtt_client.on_message = on_message
    
    # connect to the broker
    mqtt_client.connect(BROKER_URL)
    
    # subscribe to all topics
    mqtt_client.subscribe('#')
    return mqtt_client


def set_up():
    # set up the logger
    setup_logger(logger)
    
    # create the client and connect to MQTT broker
    mqtt_client = setup_MQTT_client()
    
    # wait for messages
    mqtt_client.loop_forever()


def main():
    # wait for other services to come up
    time.sleep(1)
    
    # setup MQTT client and 
    set_up()

if __name__ == "__main__":
    main()