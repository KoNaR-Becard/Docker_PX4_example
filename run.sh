#!/bin/bash

clear

xhost local:docker

if lshw -C display 2>/dev/null | grep -i "vendor" | grep -qi "nvidia"; then
    echo "NVIDIA is present as a display vendor."

    COMPOSE_FILE=compose_nvidia.yaml

else

    COMPOSE_FILE=compose_amd.yaml

fi

if [[ $1 == "pilot" ]]; then

    docker compose -f $COMPOSE_FILE exec px4_sim MicroXRCEAgent udp4 -p 8888

elif [[ $1 == "build" ]]; then

    docker compose -f $COMPOSE_FILE build

else

    docker compose -f $COMPOSE_FILE up

fi
