# IoT Platform using Microservices - SPRC

> Name: *Dumitrescu Alexandra*  
> Date: *November 2023*

## Content
<ol>
  <li>Project Structure</li>
  <li>Implementation
    <ol>
      <li>Microservices</li>
      <li>Run & cleanup commands</li>
      <li>Client tester & Testing</li>
    </ol>
  </li>
  <li>Links</li>
</ol>

## Project Structure
**server/** - Implements the adaptor used for parsing messages received from the MQTT broker and adding them  
        to the Influx-DB database  
**influx-db/** - Initial script for creating the database where the measurements will be stored **IoTSPRC**  
**client/UPB** - Testing script  
**grafana/** - dashboards/ - JSON used for creating the Battery Dashboard and UPB IoT Dashboard  
        provisioning/ - .yml files used for connecting to the Influx DB and setting path to the JSON files for the dashboards


## Implementation

### Microservices
**MQTT Broker** on port 1883, used eclipse mosquitto image  
**Grafana** on port 80  
**InfluxDB** in the ./influx-db folder there is an initial script for creating the **IoTSPRC** database.
**Adaptor** communicates with the MQTT broker and with Influx DB service. Receives message on the following format:
> <location/station> **topic**  
> single-level JSON **payload**  

All the values in the payload having type int or float will be added in the database.  
We propose a solution with common measurement for all data being stored - IoT, where we add the data having the tags: location, station, key, <station.key>  
and the value the received data.  
The adaptor also prints logging info if DEBUG_DATA_FLOW is set to "true". Run the following command to see the logs:
> docker service logs sprc3_adaptor-server  

### Run & cleanup commands
In the main directory there are 2 bash scripts used for running and cleanup. Before running make sure to set the SPRC_DVP environment variable.  
When running the cleanup script, the volumes will be deleted.

### Client tester & Testing
In the **client/UPB** there is a python script used for testing. There are 2 locations and 3 stations:
> location = ["UPB", "Test"]  
> stations = ["Gas", "Mongo", "Tel"] 

For each pair of <location/station> I randomly generate float/integer values and strings.  
I also send items to a "Dummy" topic in order to check the restriction on the payload.  
For testing and simulationg just run the client.py script.

## Links
> https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/  
> https://medium.com/javarevisited/monitoring-setup-with-docker-compose-part-2-grafana-2cd2d9ff017b  
> https://stackoverflow.com/questions/61097164/docker-stack-deploy-error-response-from-daemon-rpc-error-code-invalidargume  
> https://www.influxdata.com/blog/getting-started-python-influxdb/  
> https://www.influxdata.com/blog/how-to-setup-influxdb-telegraf-and-grafana-on-docker-part-1/  
> https://docs.python.org/3/howto/logging.html  
> https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits  
> https://stackoverflow.com/questions/63518460/grafana-import-dashboard-as-part-of-docker-compose  
> https://community.grafana.com/t/where-is-the-alias-for-flux-queries-please/44348/3  
> https://stackoverflow.com/questions/54813704/how-to-add-dashboard-configuration-json-file-in-grafana-image  