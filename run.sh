#!/bin/bash

docker build -t test-bot:0.1 click_service
docker build -t tor:0.1 tor_docker

#docker swarm leave --force
docker swarm init

#docker network rm overlay tor_network
docker network create -d overlay tor_network

docker stack deploy --compose-file="docker-compose.yaml" cr
#docker stack rm cr