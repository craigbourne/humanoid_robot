"""
Main CLI interface for the humanoid robot control system.
"""

from src.core import Robot
from src.commands import CommandProcessor

def display_help() -> None:
    # Display commands.
    print("\nAvailable commands:")
    print("  walk - Walking forward")
    print("  turn <degrees> - Turn by specified degrees")
    print("  grasp - Grip an object")
    print("  release - Release gripped object")
    print("  stop - Stop current movement")
    print("  status - Display robot status")
    print("  quit - Exit the program")
    print("  help - Show help message")


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
                print(f"Current state: {robot.current_state}")
                print(f"Operational: {robot.is_operational}")
            else:
                command_processor.enqueue_command(command)
                current_command = command_processor.process_next_command()
                
                if robot.validate_command(current_command):
                    print(f"Executing command: {current_command}")
                else:
                    print("Invalid command in current state")
                    
        except KeyboardInterrupt:
            print("\nShutting down robot system...")
            break

if __name__ == "__main__":
    main()
