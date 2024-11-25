# SLAM with DATMO Simulation

A Python-based simulation of Simultaneous Localization and Mapping (SLAM) with Detection and Tracking of Moving Objects (DATMO). This project demonstrates a robot navigating through an environment while mapping static features and tracking dynamic objects.

## Features

- Real-time simulation using Pygame
- Robot navigation with collision avoidance
- Feature extraction and mapping
- Dynamic object detection and tracking
- Interactive control of a main object using WASD keys
- Real-time proximity warnings showing:
  - Distance to nearest obstacle
  - Angle to nearest obstacle
- Visualization of:
  - Robot path
  - Sensor measurements
  - Static features
  - Dynamic objects
  - Sensor range
  - Object zones
  - Warning messages

## Requirements

- Python 3.7+
- Pygame
- NumPy

## Installation

1. Clone this repository
2. Install the required packages: 
```
pip install -r requirements.txt
```

## Usage

Run the simulation:
```
python code/slam_sim.py
```

### Controls
- W: Move main object up
- A: Move main object left
- S: Move main object down
- D: Move main object right

### Warning System
The simulation includes a real-time proximity warning system that:
- Monitors distances between the main object and surrounding obstacles
- Displays warnings when obstacles are within 30 pixels
- Shows both distance and angle to the nearest obstacle
- Updates continuously during simulation
- Appears both in the console and on-screen

## Project Structure

- `slam_sim.py`: Main simulation loop
- `env.py`: Environment setup and management
- `robot.py`: Robot class with movement and sensor integration
- `sensor.py`: ToF sensor simulation and feature extraction
- `features.py`: Feature representation and management
- `movingObjects.py`: Moving object simulation

## Configuration

Key parameters can be adjusted in the respective files:

- Sensor range: `MAX_RANGE = 100`
- Robot velocity: `ROBOT_VELOCITY = 10`
- Moving object velocity: `VELOCITY = 2`
- Number of moving objects: `NUM_MOVING_OBJECTS = 3`
- Feature association threshold: `ASSOCIATION_THRESHOLD = 10`
- Proximity warning threshold: `30 pixels`


