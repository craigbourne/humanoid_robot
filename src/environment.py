"""
Module for environmental monitoring and sensor data processing.
Simulates sensor data for robot environment awareness.
"""

from typing import Dict, List
from src.interfaces import ISensing

class EnvironmentMonitor(ISensing):
    """
    Monitors and processes environmental data for the robot.
    Implements ISensing interface for environment interaction.
    """

    def __init__(self):
        """
        Initialise the environment monitor with empty sensor readings.
        """
        self._sensor_readings: List[Dict] = []
        self._obstacle_positions: List[List[float]] = []
        self._environment_map: Dict = {}
        self._last_scan_time = 0

    def scan(self) -> Dict:
        """
        Perform an environment scan.
        Simulates sensor data collection from robot's surroundings.
        Returns: dict - Simulated sensor data including distances and obstacles
        """

        sensor_data = {
            'front_distance': 100.0,  # cm
            'left_distance': 100.0,   # cm
            'right_distance': 100.0,  # cm
            'obstacles_detected': len(self._obstacle_positions),
            'is_path_clear': True
        }

        self._sensor_readings.append(sensor_data)
        return sensor_data

    def detect(self) -> List:
        """
        Detect objects in the environment.
        Simulates object detection from sensor data.
        Returns: list - List of detected objects with their positions
        """

        # Simulate object detection
        detected_objects = []

        # This would process actual sensor data in a real-world setting
        # For now, returns an empty list indicating no objects detected
        return detected_objects

    def measure_distances(self) -> Dict[str, float]:
        """
        Measure distances in all directions.
        
        Returns: dict - Distances in centimetres for each direction
        """
        # Simulate distance measurements
        return {
            'front': 100.0,
            'left': 100.0,
            'right': 100.0,
            'back': 100.0
        }

    def update_sensor_data(self) -> None:
        """
        Update stored sensor data with new readings.
        """
        new_scan = self.scan()
        self._sensor_readings.append(new_scan)

        # Keep only the last 10 readings
        if len(self._sensor_readings) > 10:
            self._sensor_readings.pop(0)
