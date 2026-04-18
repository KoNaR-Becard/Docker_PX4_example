#!/bin/bash

if [ ! -d "$HOME/PX4-Autopilot" ]; then
    echo " Error: Folder not found ~/PX4-Autopilot"
    echo " You need to clone and build PX4 natively (make px4_sitl)"
    exit 1
fi

echo "Starting PX4-Autopilot..."

cd ~/PX4-Autopilot

pkill -9 px4
pkill -9 gz
pkill -9 ruby

export GZ_SIM_RESOURCE_PATH=$HOME/Docker_PX4_example/models:$HOME/Docker_PX4_example/worlds:$HOME/PX4-Autopilot/Tools/simulation/gz/models:$HOME/PX4-Autopilot/Tools/simulation/gz/worlds
export PX4_GZ_WORLD=$HOME/Docker_PX4_example/worlds/forest_with_panels.sdf

PX4_SYS_AUTOSTART=4001 PX4_GZ_MODEL=x500 ./build/px4_sitl_default/bin/px4