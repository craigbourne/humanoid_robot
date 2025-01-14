"""
Navigation module for humanoid robot system.
Handles position tracking, movement planning and spatial awareness.
"""

import math
from typing import Tuple, Dict, List

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

    def explain_workspace(self) -> None:
        """
        Provide a clear explanation of the workspace layout.
        """
        print("\n=== Workspace Guide ===")
        print(f"Room size: {self.room_width/100:.1f}m x {self.room_length/100:.1f}m")
        print(f"Robot starting position: Centre of room ({self.centre[0]}, {self.centre[1]})")

        print("\nObjects in workspace:")
        for obj_id, pos in self.objects.items():
            distance = math.sqrt(
                (pos[0] - self.position[0])**2 +
                (pos[1] - self.position[1])**2
            )
            direction = self.get_relative_direction(pos[0], pos[1])
            print(f"Object {obj_id}: at coordinates ({pos[0]}, {pos[1]})")
            print(f"         {distance:.0f} centimetres {direction} from robot's current position")

        print("\nNavigation:")
        print("- Coordinates are in centimetres")
        print("- (0, 0) is at the room's bottom-left corner")
        print("- Moving right increases X coordinate")
        print("- Moving forward increases Y coordinate")

        print("\nSafety Information:")
        print(f"- Robot height: {self.height}cm")
        print(f"- Robot width: {self.width}cm")
        print(f"- Minimum safe distance from objects: {self.safe_distance}cm")

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
        """
        # Check room boundaries (including robot width)
        safety_margin = self.width / 2 + self.safe_distance
        if not (safety_margin <= target_x <= self.room_width - safety_margin and
                safety_margin <= target_y <= self.room_length - safety_margin):
            return False

        # Check distance to all objects
        for pos in self.objects.values():
            distance = math.sqrt(
                (pos[0] - target_x)**2 +
                (pos[1] - target_y)**2
            )
            if distance < self.safe_distance:
                return False

        return True
