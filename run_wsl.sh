#!/bin/bash

clear

xhost local:docker

if ls /dev/dxg >/dev/null 2>&1; then
    echo "WSL GPU detected"
    COMPOSE_FILE=compose_nvidia.yaml
else
    echo "No WSL GPU"
    COMPOSE_FILE=compose_amd.yaml
fi

if [[ $1 == "pilot" ]]; then

    docker compose -f $COMPOSE_FILE exec px4_sim MicroXRCEAgent udp4 -p 8888

elif [[ $1 == "build" ]]; then

    docker compose -f $COMPOSE_FILE build

else

    docker compose -f $COMPOSE_FILE up

fi