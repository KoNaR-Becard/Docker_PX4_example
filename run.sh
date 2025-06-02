#!/bin/bash

clear

xhost local:docker

if lshw -C display 2>/dev/null | grep -i "vendor" | grep -qi "nvidia"; then
    echo "NVIDIA is present as a display vendor."

    docker compose -f compose_nvidia.yaml up
else

    docker compose -f compose_amd.yaml up
fi

