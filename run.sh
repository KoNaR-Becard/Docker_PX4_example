#!/bin/bash
set -e

# Grant Docker access to the local X11 display server
xhost +local:docker > /dev/null 2>&1

COMPOSE_FILE="compose.jazzy.yaml"
PROFILE_ARG=""

# GPU detection and profile selection
if command -v nvidia-smi > /dev/null 2>&1 && nvidia-smi > /dev/null 2>&1; then
    echo "[INFO] Dedicated NVIDIA GPU / Jetson detected. Launching with NVIDIA hardware profile..."
    PROFILE_ARG="--profile nvidia"
    SERVICE_TARGET="px4_sim_nvidia"
else
    echo "[INFO] Integrated/Universal GPU detected (Intel Arc / Lunar Lake / AMD). Launching via Mesa..."
    SERVICE_TARGET="px4_sim"
fi

case "$1" in
    build)
        docker compose -f "$COMPOSE_FILE" $PROFILE_ARG build
        ;;
    down)
        docker compose -f "$COMPOSE_FILE" $PROFILE_ARG down
        ;;
    bash)
        docker exec -it px4_sim_jazzy bash
        ;;
    *)
        echo "[INFO] Starting PX4 SITL + Gazebo Harmonic and MicroXRCEAgent..."
        docker compose -f "$COMPOSE_FILE" $PROFILE_ARG up $SERVICE_TARGET
        ;;
esac
