"""
Navigation module for humanoid robot system.
Handles position tracking, movement planning and spatial awareness.
"""

import math
from typing import Tuple, Dict, List, Optional

# pylint: disable=too-many-instance-attributes
class NavigationSystem:
    """
    Manages robot navigation, location tracking and spatial awareness.
    """

    # initialisation
    def __init__(self, room_dimensions: Tuple[float, float] = (1000, 1000)):
        """
        Initialise the navigation system with room setup and object tracking.
        Args: room_dimensions - Width and length of room in centimetres
        """
        # Room setup
        self.room_width, self.room_length = room_dimensions
        self.centre = (self.room_width / 2, self.room_length / 2)

        # Robot's current state
        self.position = list(self.centre)
        self.facing_angle = 0

        # Robot's physical dimensions
        self.height = 173  # Tesla Optimus height in centimetres
        self.width = 60   # Shoulder width in centimetres
        self.safe_distance = 100  # Minimum safe distance in centimetres

        # Storage bay is positioned in top-right corner
        self.storage_bay = [800.0, 800.0]
        self.storage_range = 50  # Distance within which storage is possible

        # Object management
        self.objects: Dict[int, List[float]] = {
            1: [300.0, 300.0],  # Bottom left quadrant
            2: [700.0, 700.0],  # Top right quadrant
            3: [300.0, 700.0]   # Top left quadrant
        }
        self.stored_objects: List[int] = []

    # navigation helpers
    def _get_direction(self, dx: float, dy: float) -> str:
        """Convert coordinate differences to compass direction."""
        if dx > 0 and dy > 0:
            return "north-east"
        elif dx > 0 and dy < 0:
            return "south-east"
        elif dx < 0 and dy > 0:
            return "north-west"
        else: return "south-west"

    def get_steps_to_object(self, obj_id: int) -> Optional[Tuple[str, int]]:
        """Calculate direction and steps to reach a specific object."""
        obj_pos = self.objects.get(obj_id)
        if not obj_pos:
            return None

        dx = obj_pos[0] - self.position[0]
        dy = obj_pos[1] - self.position[1]

        # Calculate direction based on dominant axis
        if abs(dx) > abs(dy):
            return "east" if dx > 0 else "west", int(abs(dx) / 10)
        elif abs(dy) > abs(dx):
            return "north" if dy > 0 else "south", int(abs(dy) / 10)
        else:  # Diagonal movement
            if dx > 0 and dy > 0:
                return "north-east", int(math.sqrt(dx**2 + dy**2) / 10)
            elif dx > 0 and dy < 0:
                return "south-east", int(math.sqrt(dx**2 + dy**2) / 10)
            elif dx < 0 and dy > 0:
                return "north-west", int(math.sqrt(dx**2 + dy**2) / 10)
            else:
                return "south-west", int(math.sqrt(dx**2 + dy**2) / 10)

    def get_steps_to_storage(self) -> Tuple[str, int]:
        """Calculate direction and steps to reach storage bay."""
        dx = self.storage_bay[0] - self.position[0]
        dy = self.storage_bay[1] - self.position[1]

        # Calculate steps first
        distance = math.sqrt(dx**2 + dy**2)
        steps = int(distance / 10)  # Each step is 10 centimetres

        # Determine direction based on dominant axis
        # If one axis is much larger than the other, use cardinal direction
        if abs(dx) > abs(dy) * 1.5:  # Significantly more horizontal movement
            return "east" if dx > 0 else "west", steps
        elif abs(dy) > abs(dx) * 1.5:  # Significantly more vertical movement
            return "north" if dy > 0 else "south", steps
        else:  # Truly diagonal movement
            if dx > 0 and dy > 0:
                return "north-east", steps
            elif dx > 0 and dy < 0:
                return "south-east", steps
            elif dx < 0 and dy > 0:
                return "north-west", steps
            else:
                return "south-west", steps

    def get_nearby_objects(self, max_distance: float = 200) -> Dict[int, float]:
        """Find available objects within specified distance."""
        nearby = {}
        for obj_id, pos in self.get_available_objects().items():
            distance = math.sqrt(
                (pos[0] - self.position[0])**2 +
                (pos[1] - self.position[1])**2
            )
            if distance <= max_distance:
                nearby[obj_id] = distance
        return nearby

    # movement and safety
    def is_movement_safe(self, target_x: float, target_y: float, carrying_object: bool = False) -> bool:
        """
        Determine if movement to target position is safe.
        """
        # Check room boundaries
        if not (0 <= target_x <= self.room_width and
                0 <= target_y <= self.room_length):
            return False

        # When carrying an object, prevent moving away from storage bay
        if carrying_object and not self.is_at_storage_bay(self.position):
            # Calculate if we're moving closer to storage bay
            current_distance = math.sqrt(
                (self.storage_bay[0] - self.position[0])**2 +
                (self.storage_bay[1] - self.position[1])**2
            )
            target_distance = math.sqrt(
                (self.storage_bay[0] - target_x)**2 +
                (self.storage_bay[1] - target_y)**2
            )
            # Only allow movement that gets us closer to storage bay
            if target_distance >= current_distance:
                return False

        return True

    def walk(self, direction: str, steps: int) -> bool:
        """
        Move in specified direction, adjusting for diagonal movement.
        """
        # Calculate step size (shorter for diagonal movement)
        step_size = 10  # Base step size in centimetres
        if "north" in direction and ("east" in direction or "west" in direction):
            step_size = step_size / math.sqrt(2)

        # Calculate movement
        dx = dy = 0
        if "north" in direction:
            dy = steps * step_size
        if "south" in direction:
            dy = -steps * step_size
        if "east" in direction:
            dx = steps * step_size
        if "west" in direction:
            dx = -steps * step_size

        target_x = self.position[0] + dx
        target_y = self.position[1] + dy

        if self.is_movement_safe(target_x, target_y):
            self.position = [target_x, target_y]
            return True
        return False

    # object and storage management
    def is_at_storage_bay(self, position: List[float]) -> bool:
        """
        Check if the given position is close enough to storage bay.
        
        """
        distance = math.sqrt(
            (position[0] - self.storage_bay[0])**2 +
            (position[1] - self.storage_bay[1])**2
        )
        return distance <= self.storage_range

    def store_object(self, object_id: int) -> bool:
        """
        Mark an object as stored and remove it from available objects.
        Returns True if all objects are now stored.
        """
        if object_id not in self.stored_objects:
            self.stored_objects.append(object_id)
            return len(self.stored_objects) == len(self.objects)
        return False

    def get_available_objects(self) -> Dict[int, List[float]]:
        """Get list of objects not yet stored."""
        return {obj_id: pos for obj_id, pos in self.objects.items()
                if obj_id not in self.stored_objects}

    # ui
    def explain_workspace(self) -> None:
        """
        Provide clear explanation of the workspace and available objects.
        """
        print(f"\nRoom size: {self.room_width/100:.0f}m x {self.room_length/100:.0f}m")
        print("Robot at centre of room")

        available = self.get_available_objects()
        if available:
            print("\nAvailable Objects:")
            for obj_id, pos in available.items():
                direction, steps = self.get_steps_to_object(obj_id)
                print(f"Object {obj_id}: {steps} steps {direction}")

        print("\nStorage Bay: Located in the north-east corner")
        direction, steps = self.get_steps_to_storage()
        print(f"Currently {steps} steps {direction} from robot")
