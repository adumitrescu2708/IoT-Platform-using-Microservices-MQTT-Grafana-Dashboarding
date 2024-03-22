'''
    Copyright: Dumitrescu Alexandra - Jan 2024
'''
import paho.mqtt.client as mqtt
import time, datetime, random, string, json, pytz

# data used to connect to the MQTT broker
BROKER_URL      = "localhost"
DATABASE_PORT   = 8086

def generate_random_attrs():
    # random attributes for GAS station
    attrs_GAS = {
        "BAT" : random.uniform(0.0, 100.0), # generate random BAT - float number
        "TEMP": random.randint(0, 50),      # generate random TEMP - int number
        "CONN" : ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10)), # generate random string - This should not be written in the database, only numbers
        "timestamp": (datetime.datetime.now(pytz.utc) - datetime.timedelta(0, random.randint(0, 600))).strftime("%Y-%m-%dT%H:%M:%S") + "-02:00" # generate random timestamp, close to current one
    }
    
    # random attributes for MONGO station
    attrs_MONGO = {
        "BAT" : random.uniform(0.0, 100.0), # generate random BAT - float number
        "CO2" : random.randint(0, 50),      # generate random CO2 - int number
        "TEMP": random.randint(0, 50),      # generate random TEMP - int number
        "TEST" : ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5)), # generate random string - This should not be written in the database, only numbers
        "timestamp": (datetime.datetime.now(pytz.utc)).strftime("%Y-%m-%dT%H:%M:%S") + "-02:00" # generate random timestamp, close to current one
    }
    
    # random attributes for tel station
    attrs_TEL = {
        "BAT" : random.uniform(0.0, 100.0), # generate random BAT - float number
        "NO2": random.uniform(0.0, 100.0),  # generate random NO2 - int number
        "TEMP": random.randint(0, 50)       # generate random TEMP - int number
    }
    
    attrs = [attrs_GAS, attrs_MONGO, attrs_TEL]
    return attrs

def set_up():
    # create MQTT client for sending continously data
    mqtt_client = mqtt.Client()
    mqtt_client.connect(BROKER_URL)
    mqtt_client.loop_start()
    
    # list of used locations
    location = ["UPB", "Test"]
    
    # list of used stations
    stations = ["Gas", "Mongo", "Tel"]
    time.sleep(2)
    idx = 0
    idx_location = 0
    while(1):
        # generate random attributes for the JSON sent by each location
        attrs = generate_random_attrs()
        
        # for each location send the data for the stations
        while not idx == 3:
            mqtt_client.publish(location[0] + "/" + stations[idx], json.dumps(attrs[idx]))
            print(location[0] + "/" + stations[idx] + " published " + json.dumps(attrs[idx]))
            time.sleep(2)
            
            mqtt_client.publish(location[1] + "/" + stations[idx], json.dumps(attrs[idx]))
            print(location[1] + "/" + stations[idx] + " published " + json.dumps(attrs[idx]))
            time.sleep(2)
            
            # test payload that does not respect the convention - This should not be written in the database
            mqtt_client.publish("Dummy", json.dumps(attrs[idx]))
            print("Dummy" + " published " + json.dumps(attrs[idx]))
            time.sleep(2)     
            
            idx += 1
        
        idx = 0
        
    mqtt_client.loop_stop()
    

def main():
    set_up()

if __name__ == "__main__":
    main()