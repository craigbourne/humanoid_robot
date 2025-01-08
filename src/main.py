"""
Main CLI interface for the humanoid robot control system.Provides command-line interaction with robot and navigation capabilities.
"""

import sys
import os
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import Robot
from src.commands import CommandProcessor
from src.navigation import NavigationSystem

def display_help() -> None:
    print("\nAvailable commands:")
    print("  scan - Scan surroundings for objects and obstacles")
    print("  walk to X Y - Walking to position X,Y in centimetres (e.g. 'walk to 600 700')")
    print("  turn N - Turn N degrees clockwise (e.g. 'turn 90' to turn right, 'turn -90' to turn left)")
    print("  detect - Look for objects within gripping range")
    print("  grasp - Attempt to grip nearby object")
    print("  release - Let go of held object")
    print("  where - Show distance and direction to all known objects")
    print("  status - Show current position, nearby objects and surroundings")
    print("  help - Show this guide")
    print("  quit - Exit program")

def main():
    """Main control loop for robot system."""
    # Initialise systems
    robot = Robot()
    command_processor = CommandProcessor()
    navigation = NavigationSystem()
    
    print("\nStarting Humanoid Robot Control System...")
    if robot.initialise():
        print("\nRobot system initialised successfully.")
        navigation.explain_workspace()
        display_help()
    else:
        print("Robot initialisation failed.")
        return

    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            parts = command.split()
            
            if not parts:
                continue
                
            if command == "quit":
                break
                
            elif command == "help":
                display_help()
                
            elif command == "status":
                print(navigation.get_location_summary())
                
            elif command == "where":
                nearby = navigation.get_nearby_objects(max_distance=500)
                if nearby:
                    print("\nDetected Objects:")
                    for obj_id, distance in nearby.items():
                        pos = navigation.objects[obj_id]
                        direction = navigation.get_relative_direction(pos[0], pos[1])
                        print(f"Object {obj_id}: {direction}, {distance:.0f}cm away")
                else:
                    print("\nNo objects detected within 5 metres")
                    
            elif parts[0] == "walk" and len(parts) == 4 and parts[1] == "to":
                try:
                    target_x = float(parts[2])
                    target_y = float(parts[3])
                    
                    if navigation.is_movement_safe(target_x, target_y):
                        print(f"\nMoving to position ({target_x}, {target_y})")
                        # Simulate movement with position updates
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
                            
                        print("\nMovement complete")
                    else:
                        print("\nCannot move there - path blocked or outside safe area")
                except ValueError:
                    print("\nInvalid coordinates. Use numbers for X and Y positions")
                    
            elif parts[0] == "turn":
                try:
                    degrees = float(parts[1]) if len(parts) > 1 else 90
                    direction = "right" if degrees > 0 else "left"
                    navigation.facing_angle = (navigation.facing_angle + degrees) % 360
                    print(f"\nTurned {abs(degrees)} degrees {direction}")
                    print(f"Now facing {navigation.facing_angle} degrees")
                except ValueError:
                    print("\nInvalid angle. Please specify degrees to turn")
                    
            elif command == "scan":
                print("\nScanning surroundings...")
                sleep(1)  # Simulate scanning time
                print(navigation.get_location_summary())
                
            elif command == "detect":
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
                    
            elif command == "grasp":
                grippable = navigation.get_nearby_objects(max_distance=100)
                if grippable:
                    print("\nGripping nearest object")
                    robot._object_handler._gripper_status = True
                    print("Object gripped successfully")
                else:
                    print("\nNo objects within gripping range (100cm)")
                    
            elif command == "release":
                if robot._object_handler._gripper_status:
                    robot._object_handler._gripper_status = False
                    print("\nObject released")
                else:
                    print("\nNo object currently held")
                    
            else:
                print("\nUnknown command. Type 'help' for available commands")
                
        except KeyboardInterrupt:
            print("\nShutting down robot system...")
            break

if __name__ == "__main__":
    main()
