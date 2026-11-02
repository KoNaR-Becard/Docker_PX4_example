# Becard Drone Simulation Platform

Containerized simulation stack for the Becard drone platform based on Ubuntu 24.04, ROS 2 Jazzy Jalisco, PX4 Autopilot SITL, and Gazebo Harmonic.

---

## Architecture Overview

- **Autopilot:** PX4 Autopilot SITL (v1.14 / main)
- **Airframe Model:** Custom multirotor frame (`gz_becard`)
- **Simulation Engine:** Gazebo Harmonic (8.x)
- **DDS Bridge:** Micro XRCE-DDS Agent on UDP port 8888
- **Ground Control:** MAVLink protocol on UDP port 14550
- **ROS Middleware:** ROS 2 Jazzy with pre-compiled `px4_msgs`

---

## Prerequisites

Ensure the following tools are installed on the host machine:

- Linux OS (Ubuntu 22.04 LTS or 24.04 LTS recommended)
- Docker Engine (version 24.0 or newer)
- Docker Compose v2 plugin (version 2.20 or newer)
- QGroundControl (QGC) installed natively on the host
- Display server: X11 with local access enabled

Supported GPU hardware:
- Intel Arc / Lunar Lake (via Mesa drivers and `/dev/dri`)
- AMD Radeon (via Mesa drivers and `/dev/dri`)
- NVIDIA GPUs / Jetson (via `nvidia-container-toolkit`)

---

## Quick Start

### 1. Launch Simulation and DDS Bridge

Execute the startup script from the root repository directory:

```bash
./run.sh
```

The script automatically:
1. Grants X11 access to the Docker daemon via `xhost +local:docker`.
2. Identifies host GPU architecture and applies the correct compose profile.
3. Starts the `micro_xrce_bridge` service listening on UDP port 8888.
4. Starts the `px4_sim_jazzy` service, launching PX4 SITL and Gazebo Harmonic with the `gz_becard` model.

To terminate all running containers:

```bash
./run.sh down
```

### 2. Manual Flight Verification via QGroundControl

1. Start QGroundControl on the host system.
2. The GCS automatically connects over UDP port 14550.
3. Confirm vehicle state transition to `Ready | Hold`.
4. Engage the `Takeoff` action in QGC to verify basic flight dynamics in Gazebo.

---

## Development Workflow and Onboarding Task

Application source code is located in `./workspace/src/` on the host machine. This directory is bind-mounted directly to `/app/ros2_ws/src/` inside the simulation container. Modifications made in host editors (e.g., VS Code) reflect immediately inside the running container.

### Onboarding Task: Fix Autonomous Flight Node

The repository includes a template flight control package (`drone_controller`), which currently fails to take off due to a QoS reliability mismatch with PX4 telemetry topics.

1. Open an interactive shell session inside the running container:

   ```bash
   ./run.sh bash
   ```

2. Inspect the source code in `workspace/src/Drone_Control_Node/` on your host machine. Update the telemetry topic subscriptions from the default `Reliable` profile to `SensorDataQoS` (refer to the **Critical Integration Requirements** section below).

3. Compile the package inside the container (note that `px4_msgs` is already pre-compiled at `/app/px4_msgs_ws` and sourced automatically):

   ```bash
   colcon build --packages-select drone_controller
   source install/setup.bash
   ```

4. Run the node and verify autonomous takeoff:

   ```bash
   ros2 run drone_controller drone_controller
   ```

   *Acceptance criteria:* No QoS reliability warnings appear in the console, the vehicle transitions to `Offboard` mode in QGC, and the drone climbs to its target altitude in Gazebo without timing out.

---

## Critical Integration Requirements

### QoS Policy Matching

PX4 uXRCE-DDS publishers transmit telemetry topics (`/fmu/out/*`, such as `/fmu/out/vehicle_local_position_v1`) using the `Best Effort` reliability policy.

ROS 2 subscriber nodes must configure their QoS profile accordingly:

```cpp
auto qos = rclcpp::SensorDataQoS();
subscription_ = this->create_subscription<px4_msgs::msg::VehicleLocalPosition>(
    "/fmu/out/vehicle_local_position_v1", qos, ...);
```

Using default `Reliable` QoS policies will cause DDS connection drops (`RELIABILITY_QOS_POLICY` mismatch) and prevent topic reception.

---

## CLI Reference

| Command | Action |
| :--- | :--- |
| `./run.sh` | Launch full simulation stack and DDS bridge |
| `./run.sh bash` | Attach interactive Bash shell to running simulation container |
| `./run.sh build` | Rebuild local container images |
| `./run.sh down` | Stop and tear down running containers |