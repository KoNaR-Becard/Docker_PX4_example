# PX4 Docker simulation example

## Quickstart

A simple Docker containter, based on althack/ros2:humble-cuda-gazebo image, to run PX4 simulation in Gazeboo Ignition.
In order to run simulation type:

```bash
./run.sh
```

## Running with PX4 autopilot

In second terminal run:

```bash
./run.sh pilot
```

## World selection

By default a standard plain world is used, but avaliable worlds are present in the folder `./worlds`.

To select a world, open `entrypoint.sh` file and then change a world name in 
`PX4_GZ_WORLD` variable. A world name should not have any file extension.
