#!/bin/bash
set -e

# Source ROS 2 Jazzy
source /opt/ros/jazzy/setup.bash

# Export Gazebo Paths
export GZ_SIM_RESOURCE_PATH="/app/PX4-Autopilot/Tools/simulation/gz/models:/app/PX4-Autopilot/Tools/simulation/gz/worlds:${GZ_SIM_RESOURCE_PATH}"

# Execute Entrypoint Command
cd /app/PX4-Autopilot
exec "$@"
