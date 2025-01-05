"""
Basic tests to verify core robot system functionality.
"""

from src.core import Robot

def main():
    print("Testing Robot System Implementation...")
    print("-" * 50)
    
    # Create robot instance
    print("Creating robot instance...")
    robot = Robot()
    print(f"Robot created. Initial state: {robot.current_state}")
    print(f"Is operational: {robot.is_operational}")
    
    # Try initialisation
    print("\nInitialising robot...")
    init_success = robot.initialise()
    print(f"Initialisation successful: {init_success}")
    print(f"New state: {robot.current_state}")
    print(f"Is operational: {robot.is_operational}")
    
    # Test command validation
    print("\nTesting command validation...")
    test_commands = ["walk", "turn", "grasp", "invalid_command"]
    for command in test_commands:
        is_valid = robot.validate_command(command)
        print(f"Command '{command}' is valid: {is_valid}")

if __name__ == "__main__":
    main()
