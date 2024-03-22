#! /bin/bash

mkdir "./volumes"
mkdir "./volumes/influxdb"
mkdir "./volumes/grafana"

docker compose -f stack.yml build
docker swarm init
docker stack deploy -c stack.yml sprc3
