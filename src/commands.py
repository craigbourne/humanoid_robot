"""
Module for processing and managing robot commands.
Implements command queuing and operation tracking.
"""

from collections import deque
from typing import Optional, List, Deque

class CommandProcessor:
    """
    Processes and manages robot commands using queue and stack data structures.
    Handles command validation and operation sequencing.
    """

    def __init__(self):
        """
        Initialise command processor with queue and stack structures.
        """
        self._command_queue: Deque[str] = deque()  # Queue for incoming commands
        self._operation_stack: List[str] = []      # Stack for tracking operations
        self._last_command: Optional[str] = None

    def enqueue_command(self, command: str) -> bool:
        """
        Add a command to the processing queue.
        Args: command Command to be queued
        Returns: bool - True if command was queued successfully
        """
        try:
            self._command_queue.append(command)
            return True
        except (MemoryError, RuntimeError):
            return False

    def process_next_command(self) -> Optional[str]:
        """
        Process the next command in the queue.
        Returns: str or None - Next command if available, None if queue is empty
        """
        if self._command_queue:
            command = self._command_queue.popleft()  # FIFO queue behaviour
            self._last_command = command
            self._operation_stack.append(command)    # Track operation
            return command
        return None

    def undo_last_operation(self) -> Optional[str]:
        """
        Pop the last operation from the stack.
        
        Returns: str or None - Last operation if available, None if stack is empty
        """
        if self._operation_stack:
            return self._operation_stack.pop()  # LIFO stack behaviour
        return None

    def get_operation_history(self) -> List[str]:
        """
        Get the history of operations.
        Returns: list - List of operations in chronological order
        """
        return self._operation_stack.copy()

    def clear_queue(self) -> None:
        """
        Clear all pending commands from the queue.
        """
        self._command_queue.clear()

    def queue_size(self) -> int:
        """
        Get the number of commands waiting in the queue.
        Returns: int - Number of queued commands
        """
        return len(self._command_queue)

    def stack_size(self) -> int:
        """
        Get the number of operations in the stack.
        Returns: int - Number of tracked operations
        """
        return len(self._operation_stack)
