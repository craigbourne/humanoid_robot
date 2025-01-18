"""
Main CLI interface for the humanoid robot control system.
Provides command-line interaction with robot and navigation capabilities.
"""

import sys
import os
from typing import List

from src.core import Robot
from src.navigation import NavigationSystem

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def display_help() -> None:
    """Display available commands and their usage."""
    print("\nCommands:")
    print("  walk <direction> <steps> - e.g., 'walk north-west 150'")
    print("  scan    - Check surroundings")
    print("  detect  - Look for nearby objects")
    print("  grasp   - Pick up object")
    print("  release - Let go of object")
    print("  help    - Show commands")
    print("  quit    - Exit")
    print("\nDirections: north, north-east, east, south-east, south, south-west, west, north-west")

def handle_movement(parts: List[str], navigation: NavigationSystem) -> None:
    """Handle walk <direction> <steps> command."""
    try:
        if len(parts) != 3:
            print("\nInvalid command. Use 'walk <direction> <steps>'")
            return

        direction = parts[1]
        steps = int(parts[2])

        if navigation.walk(direction, steps):
            print(f"\nMoving {steps} steps {direction}")
            current_pos = navigation.position
            print(f"Now at position ({current_pos[0]:.0f}, {current_pos[1]:.0f})")

            # Check for nearby objects
            nearby = navigation.get_nearby_objects(max_distance=100)
            if nearby:
                for obj_id in nearby:
                    print(f"Object {obj_id} is within gripping range")
        else:
            print("\nCannot move there - path blocked or outside safe area")
    except ValueError:
        print("\nInvalid number of steps. Use whole numbers only")

def handle_object_detection(navigation: NavigationSystem) -> None:
    """Handle object detection command."""
    nearby = navigation.get_nearby_objects(max_distance=150)
    if nearby:
        print("\nObjects within reach:")
        for obj_id, distance in nearby.items():
            direction, steps = navigation.get_steps_to_object(obj_id)
            print(f"Object {obj_id}: {steps} steps {direction}")
            if distance <= 100:
                print("- Within gripping range")
    else:
        print("\nNo objects within reach")

def handle_object_interaction(command: str, robot: Robot, navigation: NavigationSystem) -> None:
    """Handle grasp and release commands."""
    if command == "grasp":
        grippable = navigation.get_nearby_objects(max_distance=100)
        if grippable:
            print("\nPicking up object")
            robot.grip_object()
            print("Object gripped successfully")
        else:
            print("\nNo objects within reach")
    elif command == "release":
        if robot.is_holding_object():
            robot.release_object()
            print("\nObject released")

            # Immediate feedback about the released object's position
            nearby = navigation.get_nearby_objects(max_distance=100)
            if nearby:
                print("Object remains within gripping range")
            else:
                print("Object is no longer within gripping range")
        else:
            print("\nNo object currently held")

def handle_scan(navigation: NavigationSystem) -> None:
    """Handle scan command."""
    print("\nScanning surroundings...")
    pos = navigation.position
    print(f"Current position: ({pos[0]:.0f}, {pos[1]:.0f})")

    # Report nearby objects with directions and gripping status
    nearby = navigation.get_nearby_objects(max_distance=100)
    for obj_id in navigation.objects:
        direction, steps = navigation.get_steps_to_object(obj_id)
        status = "GRIPPABLE" if obj_id in nearby else "out of reach"
        print(f"Object {obj_id}: {steps} steps {direction} ({status})")

def handle_where(navigation: NavigationSystem) -> None:
    """Handle where command."""
    for obj_id in navigation.objects:
        direction, steps = navigation.get_steps_to_object(obj_id)
        print(f"Object {obj_id}: {steps} steps {direction}")

# pylint: disable=too-many-branches
def main() -> None:
    """Main control loop for robot system."""
    robot = Robot()
    navigation = NavigationSystem()

    print("\n=== Robot Control System ===")
    if not robot.initialise():
        print("Robot initialisation failed.")
        return

    navigation.explain_workspace()
    display_help()

    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            parts = command.split()

            if not parts:
                continue

            if command == "quit":
                break

            if command == "help":
                display_help()
            elif command == "status":
                print(f"Position: ({navigation.position[0]:.0f}, {navigation.position[1]:.0f})")
            elif command == "where":
                handle_where(navigation)
            elif command == "scan":
                handle_scan(navigation)
            elif command == "detect":
                handle_object_detection(navigation)
            elif command in ["grasp", "release"]:
                handle_object_interaction(command, robot, navigation)
            elif parts[0] == "walk":
                handle_movement(parts, navigation)
            else: print("\nUnknown command. Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nShutting down robot system...")
            break

if __name__ == "__main__":
    main()
