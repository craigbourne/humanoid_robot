"""
This module contains the abstract base class for the robot system.
AbstractRobot serves as a template that defines behaviour all robot implementations must provide.
"""

from abc import ABC, abstractmethod
from src.safety import SafetyController
from src.environment import EnvironmentMonitor
from src.motion import RobotMotion
from src.object_handling import ObjectHandler

# pylint: disable=too-many-instance-attributes

class AbstractRobot(ABC):
    """
    Abstract base class defining core robot functionality.
    Structure for robot implementations, ensuring consistent behaviour across robot types.
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

    @abstractmethod
    def get_current_state(self) -> str:
        """
        Retrieve the robot's current operational state.
        Must be implemented by concrete classes to reflect their specific states.
        Returns: str - Current state of the robot (e.g., 'Idle', 'Walking', 'Error')
        """

    @abstractmethod
    def validate_command(self, command: str) -> bool:
        """
        Validate whether a command can be executed in the current state.
        Must be implemented by concrete classes to check their specific command rules.
        Args: command - The command to validate
        Returns: bool - True if command is valid in current state, False otherwise
        """

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

class Robot(AbstractRobot):
    """
    Concrete implementation of the robot system.
    Coordinates all robot subsystems and implements required abstract methods.
    """

    def __init__(self):
        """
        Initialise the robot with all required subsystems.
        Sets up safety, environment monitoring, motion and object handling.
        """
        super().__init__()  # Initialise the parent class
        # Initialise subsystems
        self._safety = SafetyController()
        self._environment = EnvironmentMonitor()
        self._motion = RobotMotion()
        self._object_handler = ObjectHandler()
        self._current_position = [0, 0, 0]  # x, y, z coordinates
        self._current_orientation = [0, 0, 0]  # roll, pitch, yaw

    def initialise(self) -> bool:
        """
        Perform full robot initialisation sequence.
        Returns: bool - True if initialisation successful, False otherwise
        """
        try:
            # Check all subsystems
            if (self._safety.initialise() and self._environment and
                self._motion and self._object_handler):
                self._is_operational = True
                self._current_state = "Idle"
                return True
            return False
        except (AttributeError, RuntimeError):  # Specific exceptions
            self._is_operational = False
            self._current_state = "Error"
            return False

    def get_current_state(self) -> str:
        """
        Get the robot's current operational state.
        
        Returns: str - Current state of the robot
        """
        return self._current_state

    def validate_command(self, command: str) -> bool:
        """
        Check if a command can be executed in the current state.
        Args: command - Command to validate
        Returns: bool - True if command is valid, False otherwise
        """
        if not self.is_operational:
            return False

        # Basic command validation based on current state
        valid_commands = {
            "Idle": ["walk", "turn", "grasp"],
            "Walking": ["stop", "turn"],
            "Turning": ["stop", "walk"],
            "Grasping": ["release"],
            "Error": ["reset"]
        }

        return command in valid_commands.get(self._current_state, [])

    def grip_object(self) -> bool:
        """
        Attempt to grip an object.
        Returns: bool - True if grip successful, False otherwise
        """
        return self._object_handler.grip()

    def release_object(self) -> bool:
        """
        Release currently held object.
        Returns: bool - True if release successful, False otherwise
        """
        return self._object_handler.release()

    def is_holding_object(self) -> bool:
        """
        Check if robot is currently holding an object.
        Returns: bool - True if object is held, False otherwise
        """
        return self._object_handler._gripper_status
