"""
Main CLI interface for the humanoid robot control system.
Provides command-line interaction with robot and navigation capabilities.
"""

import sys
import os
from time import sleep
from typing import List

from src.core import Robot
from src.navigation import NavigationSystem

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def display_help() -> None:
    """Display available commands and their usage."""
    print("\nAvailable commands:")
    print("  scan - Scan surroundings for objects and obstacles")
    print("  walk to X Y - Walking to position ('walk to 600 700')")
    print("  turn N - Turn N deg clockwise ('turn 90' to turn right, 'turn -90' to turn left)")
    print("  detect - Look for objects within gripping range")
    print("  grasp - Attempt to grip nearby object")
    print("  release - Let go of held object")
    print("  where - Show distance and direction to all known objects")
    print("  status - Show current position, nearby objects and surroundings")
    print("  help - Show this guide")
    print("  quit - Exit program")

def handle_movement(parts: List[str], navigation: NavigationSystem) -> None:
    """Handle walk to X Y command."""
    try:
        target_x = float(parts[2])
        target_y = float(parts[3])

        if navigation.is_movement_safe(target_x, target_y):
            print(f"\nMoving to position ({target_x}, {target_y})")
            simulate_movement(navigation, target_x, target_y)
            print("\nMovement complete")
        else:
            print("\nCannot move there - path blocked or outside safe area")
    except ValueError:
        print("\nInvalid coordinates. Use numbers for X and Y positions")

def simulate_movement(navigation: NavigationSystem, target_x: float, target_y: float) -> None:
    """Simulate movement with position updates."""
    current_x, current_y = navigation.position
    steps = 5
    dx = (target_x - current_x) / steps
    dy = (target_y - current_y) / steps

    for step in range(steps):
        sleep(0.5)  # Simulate movement time
        new_x = current_x + dx * (step + 1)
        new_y = current_y + dy * (step + 1)
        navigation.position = [new_x, new_y]
        print(navigation.get_location_summary())

def handle_turn(parts: List[str], navigation: NavigationSystem) -> None:
    """Handle turn command."""
    try:
        degrees = float(parts[1]) if len(parts) > 1 else 90
        direction = "right" if degrees > 0 else "left"
        navigation.facing_angle = (navigation.facing_angle + degrees) % 360
        print(f"\nTurned {abs(degrees)} degrees {direction}")
        print(f"Now facing {navigation.facing_angle} degrees")
    except ValueError:
        print("\nInvalid angle. Please specify degrees to turn")

def handle_object_detection(navigation: NavigationSystem) -> None:
    """Handle object detection command."""
    nearby = navigation.get_nearby_objects(max_distance=150)
    if nearby:
        print("\nObjects within reach:")
        for obj_id, distance in nearby.items():
            pos = navigation.objects[obj_id]
            direction = navigation.get_relative_direction(pos[0], pos[1])
            print(f"Object {obj_id}: {direction}, {distance:.0f}cm away")
            if distance <= 100:
                print("- Within gripping range")
    else:
        print("\nNo objects detected within 1.5 metres")

def handle_object_interaction(command: str, robot: Robot,
                            navigation: NavigationSystem) -> None:
    """Handle grasp and release commands."""
    if command == "grasp":
        grippable = navigation.get_nearby_objects(max_distance=100)
        if grippable:
            print("\nGripping nearest object")
            robot.grip_object()
            print("Object gripped successfully")
        else:
            print("\nNo objects within gripping range (100cm)")
    elif command == "release":
        if robot.is_holding_object():
            robot.release_object()
            print("\nObject released")
        else:
            print("\nNo object currently held")

def handle_scan(navigation: NavigationSystem) -> None:
    """Handle scan command."""
    print("\nScanning surroundings...")
    sleep(1)  # Simulate scanning time
    print(navigation.get_location_summary())

def handle_where(navigation: NavigationSystem) -> None:
    """Handle where command."""
    nearby = navigation.get_nearby_objects(max_distance=500)
    if nearby:
        print("\nDetected Objects:")
        for obj_id, distance in nearby.items():
            pos = navigation.objects[obj_id]
            direction = navigation.get_relative_direction(pos[0], pos[1])
            print(f"Object {obj_id}: {direction}, {distance:.0f}cm away")
    else:
        print("\nNo objects detected within 5 metres")

# pylint: disable=too-many-branches
def main() -> None:
    """Main control loop for robot system."""
    robot = Robot()
    navigation = NavigationSystem()

    print("\nStarting Humanoid Robot Control System...")
    if not robot.initialise():
        print("Robot initialisation failed.")
        return

    print("\nRobot system initialised successfully.")
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
                print(navigation.get_location_summary())
            elif command == "where":
                handle_where(navigation)
            elif command == "scan":
                handle_scan(navigation)
            elif command == "detect":
                handle_object_detection(navigation)
            elif command in ["grasp", "release"]:
                handle_object_interaction(command, robot, navigation)
            elif parts[0] == "walk" and len(parts) == 4 and parts[1] == "to":
                handle_movement(parts, navigation)
            elif parts[0] == "turn":
                handle_turn(parts, navigation)
            else:
                print("\nUnknown command. Type 'help' for available commands")

        except KeyboardInterrupt:
            print("\nShutting down robot system...")
            break

if __name__ == "__main__":
    main()
