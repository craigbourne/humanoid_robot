"""
This module defines the core interfaces for the robot system.
Each interface establishes a contract that implementing classes must fulfil.
"""

from abc import ABC, abstractmethod

class IGrippable(ABC):
    """
    Interface for objects that can perform gripping actions.
    Ensures implementing classes provide methods for gripping & releasing objects safely.
    """

    @abstractmethod
    def grip(self) -> bool:
        """
        Activate the gripping mechanism.
        Returns: bool - True if gripping successful, False otherwise
        """

    @abstractmethod
    def release(self) -> bool:
        """
        Release the gripping mechanism.
        Returns: bool - True if release successful, False otherwise
        """

class IMoveable(ABC):
    """
    Interface for objects that can perform movement operations.
    Ensures implementing classes provide methods for controlled movement & stopping.
    """

    @abstractmethod
    def move(self) -> bool:
        """
        Initiate movement operation.
        Returns: bool - True if movement started successfully, False otherwise
        """

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop any current movement.
        Returns: bool - True if stop successful, False otherwise
        """


class ISensing(ABC):
    """
    Interface for objects that can perform environmental sensing.
    Ensures implementing classes provide methods for scanning environment & detecting objects.
    """

    @abstractmethod
    def scan(self) -> dict:
        """
        Perform an environment scan.
        Returns: dict - Sensor data from the scan
        """

    @abstractmethod
    def detect(self) -> list:
        """
        Detect objects in the environment.
        Returns: list - List of detected objects
        """
