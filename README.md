# SLAM with DATMO Simulation

A Python-based simulation of Simultaneous Localization and Mapping (SLAM) with Detection and Tracking of Moving Objects (DATMO). This project demonstrates a robot navigating through an environment while mapping static features and tracking dynamic objects using Kalman filtering.

## Features

- Real-time simulation using Pygame
- Robot navigation with intelligent collision avoidance
- Feature extraction and mapping using Kalman filters
- Advanced dynamic object detection and tracking:
  - Velocity-based movement detection
  - Consistent movement verification
  - Dynamic object lifecycle management
- Static feature mapping with covariance updates
- Interactive control of a main object using WASD keys
- Sophisticated proximity warning system showing:
  - Distance to nearest obstacle
  - Angle to nearest obstacle in degrees
  - Real-time visual and text warnings
- Comprehensive visualization of:
  - Robot path history
  - Raw sensor measurements
  - Static features with uncertainty
  - Dynamic objects with trajectories
  - Sensor range boundaries
  - Object interaction zones
  - Warning messages

## Requirements

- Python 3.7+
- Pygame
- NumPy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/pmr123/Python_SLAM_with_DATMO.git
cd Python_SLAM_with_DATMO
```

2. Install the required packages: 
```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:
```bash
python slam_sim.py
```

### Controls
- W: Move main object up
- A: Move main object left
- S: Move main object down
- D: Move main object right

### Warning System
The simulation includes a sophisticated proximity warning system that:
- Monitors distances to all obstacles (static and dynamic)
- Displays warnings when obstacles are within 30 pixels
- Shows precise distance and bearing to the nearest obstacle
- Provides both console and on-screen visual feedback

## Project Structure

- `slam_sim.py`: Main simulation loop and program entry point
- `env.py`: Environment management, feature tracking, and dynamic object handling
- `robot.py`: Robot class with movement logic and sensor integration
- `sensor.py`: Time-of-Flight sensor simulation and feature extraction
- `features.py`: Feature representation with Kalman filter updates
- `movingObjects.py`: Dynamic object simulation and trajectory management

## Key Parameters

### Environment Settings
- `MAX_RANGE = 100`: Maximum sensor range in pixels
- `OBJ_ZONE = 50`: Object interaction zone radius
- `COLLISION_BUFFER = 15`: Collision detection buffer size

### Movement Parameters
- `ROBOT_VELOCITY = 10`: Robot movement speed
- `VELOCITY_MAIN_OBJECT = 5`: Main object movement speed
- `VELOCITY = 2`: Moving objects speed

### Feature Detection
- `ASSOCIATION_THRESHOLD = 3`: Feature association distance threshold
- `MIN_CLUSTER_SIZE = 3`: Minimum points for feature detection
- `NOISE_STD_MEAS = 0.01`: Measurement noise standard deviation

### Dynamic Object Tracking
- `MAX_HISTORY = 20`: Maximum trajectory history length
- `NUM_MOVING_OBJECTS = 3`: Number of simulated moving objects

## Implementation Details

### Feature Management
- Uses Kalman filtering for feature position updates
- Maintains covariance matrices for uncertainty estimation
- Implements feature association with distance thresholds

### Dynamic Object Tracking
- Velocity-based movement detection
- Consistent movement verification
- Automatic removal of stale tracks
- Trajectory history maintenance

## Contributing

## Configuration

Key parameters can be adjusted in the respective files:

- Sensor range: `MAX_RANGE = 100`
- Robot velocity: `ROBOT_VELOCITY = 10`
- Moving object velocity: `VELOCITY = 2`
- Number of moving objects: `NUM_MOVING_OBJECTS = 3`
- Feature association threshold: `ASSOCIATION_THRESHOLD = 3`
- Proximity warning threshold: `30 pixels`


