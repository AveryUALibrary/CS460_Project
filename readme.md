# Indoor Building Mapping and Simulation Package

## Overview

This ROS2 package simulates an indoor environment based on the floor plan of a campus building. The model incorporates realistic navigation constraints, lighting effects, and interactive door states.

The package includes scripts to build, install, and run the simulation, along with configuration files to control parameters like lighting and door states.

## Running the Simulation

### Launch the Simulation

1. In the first terminal, navigate to the project directory and run the simulation environment:
   ```bash
   ./build_and_run_simulation.sh

   # OR

   bash build_and_run_simulation.sh
   ```

   This will launch the simulated world with the modeled building and environment.

### Run the Python Program

2. In a second terminal, run the Python program for controlling the robot in the environment:
   ```bash
   ./run_python.sh

    # OR

    bash run_python.sh
   ```

   This will start the Python script that interacts with the simulation and controls a robot in the mapped environment.

## Configuration

### Adjusting Lighting
To change the lighting settings, modify the `CS460_Project/worlds/indoor_environment.wbt` file. Update the `TexturedBackgroundLight` block to adjust lighting parameters such as the texture and luminosity:

```yaml
TexturedBackgroundLight {
  texture "noon_cloudy_empty"  # Adjust the texture for different lighting conditions
  luminosity 5                 # Change the luminosity value to adjust brightness
}
```

### Adjusting Door States
To modify the door positions (open/closed states), edit the `Door` block in the `indoor_environment.wbt` file:

```yaml
Door {
  translation -10.35 -10 0
  rotation 0 0 1 1.5708
  name "door(9)"
  size 0.2 1 3
  position -1.5  # Adjust this value to open/close the door
}
```

### Controlling Traffic Lights (CrossRoadsTrafficLight)

To simulate traffic light control at intersections within the indoor environment, you can modify the `CrossRoadsTrafficLight` block in the `indoor_environment.wbt` file. This enables custom timing and signal behavior to model realistic traffic flow and robot interactions with intersections.

```yaml
CrossRoadsTrafficLight {
  name "traffic_light_1"
  translation 5 5 0  # Set location in the environment
  colors [
    "red",
    "yellow",
    "green"
  ]
  intervals [
    5,  # Duration for red light in seconds
    2,  # Duration for yellow light in seconds
    3   # Duration for green light in seconds
  ]
  state "red"  # Initial state
}
```

This configuration controls the light sequence and duration for each signal. Adjust the `intervals` and `state` parameters as needed for different timing and initial signal states. 

## File Structure

```
CS460_Project/
├── CS460_Project
│   ├── CS460_Project
│   │   ├── __init__.py
│   │   └── robobuddy.py
│   ├── launch
│   │   └── f23_robotics_launch.py   # Launch file to start the simulation
│   ├── resource
│   │   ├── CS460_Project
│   │   ├── ros2control.yml
│   │   └── turtlebot_webots.urdf
│   ├── test
│   │   ├── test_copyright.py
│   │   ├── test_flake8.py
│   │   └── test_pep257.py
│   ├── worlds
│   │   └── indoor_environment.wbt   # World file for the building environment
│   ├── LICENSE
│   ├── package.xml                  # ROS package configuration
│   ├── setup.cfg
│   └── setup.py
├── build_and_run_simulation.sh       # Script to build and run the simulation
├── readme.md                         # Documentation
├── run_local.sh
└── run_python.sh                     # Script to run the Python program
```