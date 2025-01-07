"""
Module for handling object manipulation operations.
Controls gripping mechanisms and force monitoring.
"""

from typing import Optional
from src.interfaces import IGrippable

class ObjectHandler(IGrippable):
    """
    Controls object manipulation operations including gripping and releasing.
    Implements IGrippable interface for object handling.
    """

    def __init__(self):
        """
        Initialise object handler with default parameters.
        """
        self._gripper_status: bool = False  # False = open, True = closed
        self._max_grip_force: float = 100.0  # Maximum force in Newtons
        self._current_force: float = 0.0
        self._object_held: bool = False

    def grip(self) -> bool:
        """
        Activate gripping mechanism.
        Returns: bool - True if grip successful, False otherwise
        """
        if not self._gripper_status and self._check_grip_safety():
            self._gripper_status = True
            self._object_held = True
            return True
        return False

    def release(self) -> bool:
        """
        Release gripping mechanism.
        Returns: bool - True if release successful, False otherwise
        """
        if self._gripper_status:
            self._gripper_status = False
            self._object_held = False
            self._current_force = 0.0
            return True
        return False

    def _check_grip_safety(self) -> bool:
        """
        Check if gripping operation is safe.
        Returns: bool - True if operation is safe, False otherwise
        """
        # In a real system, this would check various safety conditions
        # For now, returns True if force is within limits
        return self._current_force < self._max_grip_force

    def monitor_grip_force(self) -> float:
        """
        Monitor current grip force.
        Returns: float - Current grip force in Newtons
        """
        # In a real system, this would read from force sensors
        return self._current_force

    def adjust_grip(self, force: float) -> bool:
        """
        Adjust gripping force.
        Args: force - Target force in Newtons
        Returns: bool - True if adjustment successful
        """
        if 0 <= force <= self._max_grip_force:
            self._current_force = force
            return True
        return False
