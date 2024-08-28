import time

from amber_api.amber_robot import Amber_Robot
# Set ip address
IP_ADDR = "192.168.50.3"
# Set port
PORT = 26001
# Set joint count
joint_count = 7

arm = Amber_Robot(IP_ADDR, PORT, joint_count=joint_count)
#arm.gripper_calibrate()
arm.gripper_ctrl(action=0,force=10)

time.sleep(5)

arm.gripper_ctrl()
