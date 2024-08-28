import random
import socket
from ctypes import *

'''
An example for Cartesian control by python

Ref: https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing#4-cartesian-control

'''


class robot_cmd(Structure):  # ctypes struct for send
    _pack_ = 1  # Override Structure align
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("xyz", c_float * 3),  # ctypes array
                ("rpy", c_float * 3),
                ("arm_angle", c_float),
                ("time", c_float),
                ]


class robot_data(Structure):  # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("respond", c_uint8),
                ]


def move_c(c_pos, duration, IP_ADDR="127.0.0.1", PORT=26001):
    payloadS = robot_cmd()
    payloadS.cmd_no = 6
    payloadS.length = 40
    payloadS.counter = random.randint(0, 2147483647)
    payloadS.xyz[0] = c_pos[0]
    payloadS.xyz[1] = c_pos[1]
    payloadS.xyz[2] = c_pos[2]
    payloadS.rpy[0] = c_pos[3]
    payloadS.rpy[1] = c_pos[4]
    payloadS.rpy[2] = c_pos[5]
    payloadS.arm_angle = 0
    payloadS.time = duration

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(payloadS, (IP_ADDR, PORT))
    s.settimeout(3)
    try:
        data, addr = s.recvfrom(1024)  # Need receive return
        payloadR = robot_data.from_buffer_copy(data)  # Convert raw data into ctypes struct to print
        return payloadR.respond
    except socket.timeout:
        return False
