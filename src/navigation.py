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

    def __init__(self, room_dimensions: Tuple[float, float] = (1000, 1000)):
        """
        Set up the navigation system.
        Args: room_dimensions - Width and length of room in centimetres
        """
        # Room setup
        self.room_width, self.room_length = room_dimensions
        self.centre = (self.room_width / 2, self.room_length / 2)

        # Robot's current state
        self.position = list(self.centre)  # Start in centre of room
        self.facing_angle = 0  # 0 degrees = facing 'forward'

        # Robot's physical dimensions
        self.height = 173  # cm (Tesla Optimus height)
        self.width = 60   # cm (shoulder width)
        self.safe_distance = 100  # Minimum safe distance from objects

        # Initialise objects in the workspace
        self.objects: Dict[int, List[float]] = {
            1: [300.0, 300.0],  # Object 1 in bottom left quadrant
            2: [700.0, 700.0],  # Object 2 in top right quadrant
            3: [300.0, 700.0]   # Object 3 in top left quadrant
        }
        self.object_counter = 3

        # Add storage bay in north-east corner of room
        self.storage_bay = [800.0, 800.0]  # Positioned away from objects
        
        # Track object status
        self.stored_objects: List[int] = []  # Keep track of which objects are in storage

    def get_steps_to_object(self, obj_id: int) -> Optional[Tuple[str, int]]:
        """
        Calculate direction and steps to reach an object.
        Returns: Tuple of (direction, steps) or None if object not found
        """
        obj_pos = self.objects.get(obj_id)
        if not obj_pos:
            return None
        
        dx = obj_pos[0] - self.position[0]
        dy = obj_pos[1] - self.position[1]
        
        # Determine primary direction
        if dx > 0 and dy > 0:
            direction = "north-east"
        elif dx > 0 and dy < 0:
            direction = "south-east"
        elif dx < 0 and dy > 0:
            direction = "north-west"
        else:
            direction = "south-west"
            
        # Calculate steps (each step is 10 centimetres)
        distance = math.sqrt(dx**2 + dy**2)
        steps = int(distance / 10)
        
        return direction, steps

    def explain_workspace(self) -> None:
        """
        Provide a clear explanation of the workspace layout.
        """
        print(f"Room size: {self.room_width/100:.0f}m x {self.room_length/100:.0f}m")
        print("Robot at centre of room")
        print("\nObjects to interact with:")
        for obj_id in self.objects:
            direction, steps = self.get_steps_to_object(obj_id)
            print(f"Object {obj_id}: {steps} steps {direction}")

    def get_location_summary(self) -> str:
        """
        Provide a human-friendly summary of current location and surroundings.
        """
        nearby_objects = self.get_nearby_objects()

        summary = [
            f"\nCurrent Position: ({self.position[0]:.0f}, {self.position[1]:.0f})",
            f"Facing: {self.facing_angle} degrees",
            "\nDistance to Walls:",
            f"- Forward: {self.room_length - self.position[1]:.0f}cm",
            f"- Backward: {self.position[1]:.0f}cm",
            f"- Right: {self.room_width - self.position[0]:.0f}cm",
            f"- Left: {self.position[0]:.0f}cm"
        ]

        if nearby_objects:
            summary.extend(["\nNearby Objects:"])
            for obj_id, distance in nearby_objects.items():
                pos = self.objects[obj_id]
                direction = self.get_relative_direction(pos[0], pos[1])
                summary.append(f"- Object {obj_id}: {direction}, {distance:.0f}cm away")

        return "\n".join(summary)

    def is_at_storage_bay(self, position: List[float], tolerance: float = 50) -> bool:
        """
        Check if given position is at the storage bay.
        Uses a tolerance value to allow slight positioning variations.
        """
        distance = math.sqrt(
            (position[0] - self.storage_bay[0])**2 +
            (position[1] - self.storage_bay[1])**2
        )
        return distance <= tolerance

    def get_relative_direction(self, x: float, y: float) -> str:
        """
        Convert coordinates into human-friendly relative directions.
        """
        rel_x = x - self.position[0]
        rel_y = y - self.position[1]

        angle = math.degrees(math.atan2(rel_y, rel_x))
        relative_angle = (angle - self.facing_angle) % 360

        # Convert mathematical angle to compass direction
        if 315 <= relative_angle or relative_angle < 45:
            return "ahead"
        if 45 <= relative_angle < 135:
            return "to your right"
        if 135 <= relative_angle < 225:
            return "behind you"
        return "to your left"

    def get_nearby_objects(self, max_distance: float = 200) -> Dict[int, float]:
        """
        Find objects within specified distance of robot.
        Returns: Dictionary mapping object IDs to their distances
        """
        nearby = {}
        for obj_id, pos in self.objects.items():
            distance = math.sqrt(
                (pos[0] - self.position[0])**2 +
                (pos[1] - self.position[1])**2
            )
            if distance <= max_distance:
                nearby[obj_id] = distance
        return nearby

    def is_movement_safe(self, target_x: float, target_y: float) -> bool:
        """
        Check if movement to target position is safe.
        First checks if movement would get us within gripping range of an object.
        If not, ensures we maintain safe distance from all objects.
        """
        # First, check room boundaries
        if not (0 <= target_x <= self.room_width and 
                0 <= target_y <= self.room_length):
            return False

        # Check if we're trying to reach an object
        for obj_pos in self.objects.values():
            distance_to_object = math.sqrt(
                (obj_pos[0] - target_x)**2 + 
                (obj_pos[1] - target_y)**2
            )
            # Allow movement if it gets us within gripping range
            if distance_to_object <= 100:  # 100cm gripping range
                return True
            # If we're not trying to grip but too close, prevent movement
            if distance_to_object < self.safe_distance:
                return False

        # If not near any objects, movement is safe
        return True

    def walk(self, direction: str, steps: int) -> bool:
        """
        Move in specified direction by number of steps.
        Accounts for diagonal movement being longer than cardinal directions.
        Each step is 10 centimetres in cardinal directions, adjusted for diagonals.
        Returns: bool - True if movement successful, False otherwise
        """
        # Calculate target position based on direction and steps
        dx, dy = 0, 0
        step_size = 10  # Base step size in centimetres
        
        # For diagonal movements, adjust step size
        is_diagonal = False
        if "north" in direction and ("east" in direction or "west" in direction):
            is_diagonal = True
        if "south" in direction and ("east" in direction or "west" in direction):
            is_diagonal = True
        
        # Adjust step size for diagonal movement
        if is_diagonal:
            step_size = step_size / math.sqrt(2)
        
        # Calculate movement
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
