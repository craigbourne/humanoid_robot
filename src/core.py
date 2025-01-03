"""
This module contains the abstract base class for the robot system.
The AbstractRobot class serves as a template that defines essential behaviour all robot implementations must provide.
"""

from abc import ABC, abstractmethod
from typing import Optional

class AbstractRobot(ABC):
    """
    Abstract base class defining core robot functionality.
    This class establishes the fundamental structure for robot implementations, ensuring consistent behaviour across different robot types.
    """

    def __init__(self):
        """
        Initialise the abstract robot.
        Sets up basic attributes that all robots will need.
        """
        self._current_state = "Idle"  # Robots always start in Idle state
        self._is_operational = False  # Safety first - starts non-operational
        self._last_command = None     # Track the most recent command

    @abstractmethod
    def initialise(self) -> bool:
        """
        Perform robot initialisation sequence.
        Must be implemented by concrete classes to set up their specific requirements.
        Returns: bool - True if initialisation successful, False otherwise
        """
        pass

    @abstractmethod
    def get_current_state(self) -> str:
        """
        Retrieve the robot's current operational state.
        Must be implemented by concrete classes to reflect their specific states.
        Returns: str - Current state of the robot (e.g., 'Idle', 'Walking', 'Error')
        """
        pass

    @abstractmethod
    def validate_command(self, command: str) -> bool:
        """
        Validate whether a command can be executed in the current state.
        Must be implemented by concrete classes to check their specific command rules.
        Args: command - The command to validate
        Returns: bool - True if command is valid in current state, False otherwise
        """
        pass

    @property
    def is_operational(self) -> bool:
        """
        Check if the robot is currently operational.
        Returns: bool - True if robot is operational, False otherwise
        """
        return self._is_operational

    @property
    def current_state(self) -> str:
        """
        Get the current state of the robot.
        Returns: str - Current robot state
        """
        return self._current_state
