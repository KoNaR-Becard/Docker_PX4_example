#!/bin/bash

# Clear the terminal
clear

# GPU Detection and Compose File Selection
if grep -qi microsoft /proc/version; then
    # WSL Environment
    if ls /dev/dxg >/dev/null 2>&1; then
        echo "WSL GPU detected."
        # Prefer compose_nvidia_wsl.yaml if available, fallback to compose_nvidia.yaml
        if [ -f "compose_nvidia_wsl.yaml" ]; then
            COMPOSE_FILE=compose_nvidia_wsl.yaml
        else
            COMPOSE_FILE=compose_nvidia.yaml
        fi
    else
        echo "No WSL GPU detected."
        COMPOSE_FILE=compose_amd.yaml
    fi
else
    # Native Linux Environment
    if lshw -C display 2>/dev/null | grep -i "vendor" | grep -qi "nvidia" || command -v nvidia-smi > /dev/null; then
        echo "NVIDIA GPU detected."
        COMPOSE_FILE=compose_nvidia.yaml
    else
        echo "NVIDIA GPU not detected (falling back to AMD/Intel config)."
        COMPOSE_FILE=compose_amd.yaml
    fi
fi

echo "Using compose file: $COMPOSE_FILE"

# Grant Docker access to the X server
xhost local:docker > /dev/null 2>&1

# Execute the requested command
if [[ $1 == "pilot" ]]; then
    docker compose -f "$COMPOSE_FILE" exec px4_sim MicroXRCEAgent udp4 -p 8888
elif [[ $1 == "build" ]]; then
    docker compose -f "$COMPOSE_FILE" build
else
    docker compose -f "$COMPOSE_FILE" up
fi
