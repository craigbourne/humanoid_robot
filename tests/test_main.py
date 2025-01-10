"""
Comprehensive test suite for humanoid robot control system.
Tests all major components and their interactions using pytest.
"""

import pytest
from src.core import Robot
from src.navigation import NavigationSystem
from src.commands import CommandProcessor

class TestRobotSystem:
    """
    Test suite covering all major system components.
    Each test method validates specific functionality with clear assert statements.
    """
    
    @pytest.fixture
    def robot(self):
        # Provide a fresh robot instance for each test.
        return Robot()
        
    @pytest.fixture
    def nav_system(self):
        # Provide a navigation system instance for each test.
        return NavigationSystem()
        
    @pytest.fixture
    def cmd_processor(self):
        # Provide a command processor instance for each test.
        return CommandProcessor()

    def test_robot_initialisation(self, robot):
        # Verify robot initialises in correct starting state.
        # Initial state checks
        assert robot.current_state == "Idle", "Robot should start in Idle state"
        assert not robot.is_operational, "Robot should start non-operational"
        
        # Post-initialisation checks
        success = robot.initialise()
        assert success, "Initialisation should succeed"
        assert robot.is_operational, "Robot should be operational after initialisation"

    def test_command_validation(self, robot):
        # Test command validation in different robot states.
        robot.initialise()
        
        # Test valid commands in Idle state
        assert robot.validate_command("walk"), "Walk should be valid in Idle state"
        assert robot.validate_command("turn"), "Turn should be valid in Idle state"
        assert robot.validate_command("grasp"), "Grasp should be valid in Idle state"
        
        # Test invalid commands
        assert not robot.validate_command("jump"), "Invalid command should be rejected"
        assert not robot.validate_command(""), "Empty command should be rejected"

    def test_navigation_boundaries(self, nav_system):
        # Test navigation system's boundary checking.
        # Test safe positions
        assert nav_system.is_movement_safe(500, 500), "Centre position should be safe"
        assert nav_system.is_movement_safe(200, 200), "Position within bounds should be safe"
        
        # Test unsafe positions
        assert not nav_system.is_movement_safe(0, 0), "Position at origin should be unsafe"
        assert not nav_system.is_movement_safe(1000, 1000), "Position at max bounds should be unsafe"

    def test_command_processing(self, cmd_processor):
        # Test command queue and processing functionality.
        # Test command enqueuing
        assert cmd_processor.enqueue_command("walk to 500 500"), "Should accept valid command"
        assert cmd_processor.queue_size() == 1, "Queue should have one command"
        
        # Test command processing
        command = cmd_processor.process_next_command()
        assert command == "walk to 500 500", "Should retrieve correct command"
        assert cmd_processor.queue_size() == 0, "Queue should be empty after processing"

    def test_object_handling(self, robot):
        # Test object gripping functionality.
        robot.initialise()
        handler = robot._object_handler
        
        # Test gripping
        assert not handler._gripper_status, "Gripper should start open"
        assert handler.grip(), "Grip command should succeed"
        assert handler._gripper_status, "Gripper should be closed after grip"
        
        # Test releasing
        assert handler.release(), "Release command should succeed"
        assert not handler._gripper_status, "Gripper should be open after release"

    def test_safety_monitoring(self, robot):
        # Test safety monitoring and barrier functions.
        robot.initialise()
        safety = robot._safety
        
        # Test safety status
        assert safety.validate_safety(), "Should be safe after initialisation"
        
        # Test emergency stop
        safety.trigger_emergency_stop()
        assert not safety.validate_safety(), "Should be unsafe after emergency stop"

    def test_environment_monitoring(self, robot):
        # Test environment monitoring and sensor data processing.
        robot.initialise()
        env = robot._environment
        
        # Test scanning
        scan_data = env.scan()
        assert isinstance(scan_data, dict), "Scan should return dictionary"
        assert "front_distance" in scan_data, "Scan should include front distance"
        assert "obstacles_detected" in scan_data, "Scan should report obstacles"

    def test_movement_execution(self, robot):
        # Test movement commands and position updates.
        robot.initialise()
        
        # Test basic movement
        initial_pos = robot._current_position.copy()
        robot._motion.walk("forward")
        assert robot._motion._is_moving, "Robot should be moving"
        
        robot._motion.stop()
        assert not robot._motion._is_moving, "Robot should stop when commanded"