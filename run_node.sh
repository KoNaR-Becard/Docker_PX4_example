#!/usr/bin/env bash
set -e

CONTAINER_NAME="px4_sim_jazzy"

if [ -z "$1" ]; then
    echo "Usage:"
    echo "  ./run_node.sh <package_name> [node_name]"
    echo "  ./run_node.sh <package_name> --launch <launch_file>"
    exit 1
fi

PKG_NAME="$1"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "[ERROR] Container '${CONTAINER_NAME}' is not running. Launch simulation first: ./run.sh"
    exit 1
fi

echo "[1/2] Building package '${PKG_NAME}'..."
docker exec -it "$CONTAINER_NAME" bash -c \
    "source /opt/ros/jazzy/setup.bash && cd /app/ros2_ws && colcon build --symlink-install --packages-up-to ${PKG_NAME}"

echo ""
echo "[2/2] Starting executable..."
if [ "$2" == "--launch" ]; then
    LAUNCH_FILE="$3"
    docker exec -it "$CONTAINER_NAME" bash -c \
        "source /opt/ros/jazzy/setup.bash && cd /app/ros2_ws && source install/setup.bash && ros2 launch ${PKG_NAME} ${LAUNCH_FILE}"
else
    NODE_NAME="${2:-$PKG_NAME}"
    docker exec -it "$CONTAINER_NAME" bash -c \
        "source /opt/ros/jazzy/setup.bash && cd /app/ros2_ws && source install/setup.bash && ros2 run ${PKG_NAME} ${NODE_NAME}"
fi
