"""
Main CLI interface for the humanoid robot control system.
Controls robot operations with simulated environment awareness.
"""

import sys
import os
from time import sleep
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.core import Robot
from src.commands import CommandProcessor

def display_help() -> None:
    print("\nAvailable commands:")
    print("  scan - Scan surroundings for objects and obstacles")
    print("  walk to <x> <y> - Walking forward to specific coordinates (e.g. 'walk to 50 100' moves to point 50cm right, 100cm forward)")
    print("  turn <degrees> - Turn clockwise by degrees (e.g. 'turn 90' turns right, 'turn -90' turns left)")
    print("  detect - Look for grippable objects")
    print("  grasp - Grip detected object")
    print("  release - Release gripped object")
    print("  stop - Stop current movement")
    print("  status - Display robot position and surroundings")
    print("  quit - Exit the program")
    print("  help - Show commands")

def display_status(robot) -> None:
    print("\nRobot Status:")
    print(f"Position: {robot._current_position}")
    print(f"State: {robot.current_state}")
    
    # Environment status
    env_data = robot._environment.scan()
    print("\nEnvironment:")
    print(f"Front distance: {env_data['front_distance']}cm")
    print(f"Left distance: {env_data['left_distance']}cm")
    print(f"Right distance: {env_data['right_distance']}cm")
    print(f"Path clear: {'Yes' if env_data['is_path_clear'] else 'No'}")
    
    # Gripper status
    print("\nGripper:")
    print(f"Status: {'Closed' if robot._object_handler._gripper_status else 'Open'}")
    if robot._object_handler._object_held:
        print(f"Holding object with force: {robot._object_handler.monitor_grip_force()}N")

def parse_command(command: str) -> tuple:
    parts = command.split()
    return parts[0] if parts else "", parts[1:] if len(parts) > 1 else []

def execute_command(robot, cmd: str, args: list) -> bool:
    try:
        if cmd == "scan":
            env_data = robot._environment.scan()
            print("\nScan results:")
            print(f"Obstacles detected: {env_data['obstacles_detected']}")
            print(f"Path clear: {'Yes' if env_data['is_path_clear'] else 'No'}")
            return True
            
        elif cmd == "walk" and len(args) == 3 and args[0] == "to":
            try:
                x, y = float(args[1]), float(args[2])
                if robot._safety.check_barriers([x, y, 0]):
                    print(f"Walking to position ({x}, {y})")
                    robot._current_position[0] = x
                    robot._current_position[1] = y
                    sleep(1)  # Simulate movement
                    return True
                else:
                    print("Movement blocked by safety barrier")
                    return False
            except ValueError:
                print("Invalid coordinates")
                return False
                
        elif cmd == "detect":
            objects = robot._environment.detect()
            if objects:
                print("\nDetected objects:")
                for obj in objects:
                    print(f"- Object at position: {obj}")
            else:
                print("No objects detected in range")
            return True
            
        elif cmd == "grasp":
            if robot._object_handler.grip():
                print("Object gripped successfully")
                return True
            print("Failed to grip object")
            return False
            
        elif cmd == "release":
            if robot._object_handler.release():
                print("Object released")
                return True
            print("No object to release")
            return False
            
        elif cmd == "turn":
            try:
                degrees = float(args[0]) if args else 90.0
                if robot._motion.turn(degrees):
                    print(f"Turned {degrees} degrees")
                    return True
                print("Turn failed")
                return False
            except ValueError:
                print("Invalid angle")
                return False
                
        elif cmd == "stop":
            robot._motion.stop()
            print("Stopped all movement")
            return True
            
        return False
        
    except Exception as e:
        print(f"Error executing command: {e}")
        return False

def main():
    """Main CLI loop for robot control."""

    robot = Robot()
    command_processor = CommandProcessor()
    
    print("Initialising robot system...")
    if robot.initialise():
        print("Robot system ready.")
        display_help()
    else:
        print("Robot initialisation failed.")
        return

    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit":
                break
            elif command == "help":
                display_help()
            elif command == "status":
                display_status(robot)
            else:
                cmd, args = parse_command(command)
                if execute_command(robot, cmd, args):
                    command_processor.enqueue_command(command)
                else:
                    print("Command failed or invalid")
                    
        except KeyboardInterrupt:
            print("\nShutting down robot system...")
            break

if __name__ == "__main__":
    main()
