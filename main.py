from amber_api.amber_robot import Amber_Robot

# Set ip address
IP_ADDR = "192.168.50.3"
# Set port
PORT = 26001
# Set joint count
joint_count = 7

arm = Amber_Robot(IP_ADDR, PORT, joint_count=joint_count)
print(f"The robotic arm is now in mode{arm.get_mode()} ")
# Set robot to Position Mode
arm.set_position_mode()
# Get status from robot
j_pos, c_pos = arm.get_status()

print(f"Joint Position [1,2,3,4,5,6,7] = {j_pos})")
print(f"Cartesian Position [X,Y,Z,Roll,Pitch,Yaw] = {c_pos}")
print(f"The robotic arm is now in mode{arm.get_mode()} ")

print("Move Joint to [1,1,1,1,1,1,1]")
# Move Joint
j_target = [1, 1, 1, 1, 1, 1, 1]  # Joint Position [1,2,3,4,5,6,7]
arm.move_j(j_target, duration=3)
# Wait until finish
print("Success?")
print(arm.wait_for_joint(j_target))  # True = pass, False = timeout


print("Move Joint to Zero")
arm.move_zero()
arm.wait_for_joint([0, 0, 0, 0, 0, 0, 0])

print("Move Cartesian coordinates")
# Move Cartesian coordinates
c_target = [0, 0, 0.4, 0.2, 0, 0]  # Cartesian Position [X,Y,Z,Roll,Pitch,Yaw]
print("Is inverse kinematics correct?")
print(arm.move_c(c_target, duration=3))
# Wait until finish
print("Success?")
print(arm.wait_for_cartesian(c_target))  # True = pass, False = timeout
print("Move Joint to Zero")
# Move Back to Zero
arm.move_zero()
# Set limit
arm.joint_upper_limit = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5,0.5]
# Default =  [2.0944, 2.0944, 2.0944, 2.0944, 2.0944, 2.0944, 2.0944]
arm.joint_lower_limit = [-1, -1, -1, -1, -1, -1, -1]
# Default =  [-2.0944, -2.0944, -2.0944, -2.0944, -2.0944, -2.0944, -2.0944]

j_target = [1, 1, 1, 1, 1, 1, 1]
print(arm.move_j(j_target, duration=3))
# Will not move because it exceeds the limit

c_target = [0, 0, 0.8, 0.0, 0, 0]
print("Is inverse kinematics correct?")
print(arm.move_c(c_target, duration=3))
# Will not move because it exceeds the limit
