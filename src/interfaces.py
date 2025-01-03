"""
This module defines the core interfaces for the robot system.
Each interface establishes a contract that implementing classes must fulfil.
"""

from abc import ABC, abstractmethod


class IGrippable(ABC):
    """
    Interface for objects that can perform gripping actions.
    This interface ensures implementing classes provide methods for 
    gripping and releasing objects safely.
    """
    
    @abstractmethod
    def grip(self) -> bool:
        """
        Activate the gripping mechanism.
        Returns:bool: True if gripping successful, False otherwise
        """
        pass

    @abstractmethod
    def release(self) -> bool:
        """
        Release the gripping mechanism.
        Returns:bool: True if release successful, False otherwise
        """
        pass


class IMoveable(ABC):
    """
    Interface for objects that can perform movement operations.
    This interface ensures implementing classes provide methods for
    controlled movement and stopping.
    """
    
    @abstractmethod
    def move(self) -> bool:
        """
        Initiate movement operation.
        Returns: bool: True if movement started successfully, False otherwise
        """
        pass

    @abstractmethod
    def stop(self) -> bool:
        """
        Stop any current movement.
        Returns:bool: True if stop successful, False otherwise
        """
        pass


class ISensing(ABC):
    """
    Interface for objects that can perform environmental sensing.
    This interface ensures implementing classes provide methods for
    scanning the environment and detecting objects.
    """
    
    @abstractmethod
    def scan(self) -> dict:
        """
        Perform an environment scan.
        Returns:dict: Sensor data from the scan
        """
        pass

    @abstractmethod
    def detect(self) -> list:
        """
        Detect objects in the environment.
        Returns:list: List of detected objects
        """
        pass