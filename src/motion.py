"""
Module for controlling robot motion including walking and turning.
Implements movement with safety considerations.
"""

from typing import List, Tuple
from .interfaces import IMoveable

class RobotMotion(IMoveable):
    """
    Controls robot movement operations including walking and turning.
    Implements IMoveable interface for motion control.
    """

    def __init__(self):
        """
        Initialise motion controller with default parameters.
        """
        self._walking_speed: float = 0.0
        self._turning_angle: float = 0.0
        self._safety_boundaries: List[float] = [100.0, 100.0, 100.0]  # x, y, z limits
        self._is_moving: bool = False

    def move(self) -> bool:
        """
        Initiate movement operation.
        Returns: bool - True if movement started successfully, False otherwise
        """
        if self._check_movement_safe():
            self._is_moving = True
            return True
        return False

    def stop(self) -> bool:
        """
        Stop any current movement.
        Returns: bool - True if stop successful, False otherwise
        """
        self._walking_speed = 0.0
        self._is_moving = False
        return True

    def walk(self, direction: str) -> bool:
        """
        Walk in specified direction.
        Args: direction -'forward', 'backward'
        Returns: bool - True if walking initiated successfully
        """
        if direction not in ['forward', 'backward']:
            return False
            
        self._walking_speed = 5.0 if direction == 'forward' else -5.0
        return self.move()

    def turn(self, degrees: float) -> bool:
        """
        Turn robot by specified degrees.
        Args: degrees - Angle to turn in degrees
        Returns: bool - True if turn initiated successfully
        """
        if not -180.0 <= degrees <= 180.0:
            return False
            
        self._turning_angle = degrees
        return self.move()

    def _check_movement_safe(self) -> bool:
        """
        Check if intended movement is within safety boundaries.
        Returns: bool - True if movement is safe, False otherwise
        """
        # This would be used to check actual safety conditions in real-world setting, but for now, returns True if not already moving
        return not self._is_moving

    def maintain_stability(self) -> bool:
        """
        Maintain robot's stability during movement.
        Returns: bool - True if stability maintained, False otherwise
        """
        # Simulate stability check
        return True
