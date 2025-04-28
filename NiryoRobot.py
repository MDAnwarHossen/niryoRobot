# Imports
from pyniryo import NiryoRobot, PoseObject, ObjectColor

# - Constants
workspace_name = "works"  # Robot's Workspace Name
robot_ip_address = '10.10.10.10'  # Replace with your robot's IP

# The pose from where the image processing happens
observation_pose = PoseObject(0.19, -0.01, 0.37, 3.14, 0.0, 0.0)

# Fixed placement poses
blue_place_pose = PoseObject(
    0.01, -0.17, 0.15, 3.14, -0.01, -1.5)  # Blue goes left
red_place_pose = PoseObject(
    0.18, 0.15, 0.15, 3.14, -0.01, -1.5)  # Red goes right

max_failure_count = 3

# - Initialization
robot = NiryoRobot(robot_ip_address)
robot.calibrate_auto()       # Calibrate robot (if needed)
robot.update_tool()          # Update the tool info

try_without_success = 0

# Loop until too many failures
while try_without_success < max_failure_count:
    # Move to observation pose
    robot.move(observation_pose)

    # Try to detect and pick an object
    obj_found, shape, color = robot.vision_pick(workspace_name)

    if not obj_found:
        try_without_success += 1
        robot.wait(0.1)
        continue

    # Only process blue and red objects
    if color == ObjectColor.BLUE:
        target_pose = blue_place_pose
    elif color == ObjectColor.RED:
        target_pose = red_place_pose
    else:
        print(f"Ignored {color.name} object.")
        continue  # Skip other colors (like green)

    # Debug: Print where the object is going
    print(f"Placing {color.name} object at: {target_pose}")

    # Place the object at the target location
    robot.place(target_pose)

    try_without_success = 0

# Put the robot to sleep after the process ends
robot.go_to_sleep()
