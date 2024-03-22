#! /bin/bash
docker stack rm sprc3
sleep 2
docker compose -f stack.yml down --volumes
sleep 2
docker swarm leave --force
sleep 2
rm -rf ./volumes