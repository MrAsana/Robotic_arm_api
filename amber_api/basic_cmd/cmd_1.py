import random
import socket
from ctypes import *

'''
A simple example for controlling a single joint move once by python

Ref: https://github.com/MrAsana/AMBER_B1_ROS2/wiki/SDK-&-API---UDP-Ethernet-Protocol--for-controlling-&-programing#2-single-joint-move-once
C++ version:  https://github.com/MrAsana/C_Plus_API/tree/master/amber_gui_4_node
     
'''


class robot_cmd(Structure):  # ctypes struct for send
    _pack_ = 1  # Override Structure align
    _fields_ = [("cmd_no", c_uint16),  # Ref:https://docs.python.org/3/library/ctypes.html
                ("length", c_uint16),
                ("counter", c_uint32),
                ]


class robot_data(Structure):  # ctypes struct for receive
    _pack_ = 1
    _fields_ = [("cmd_no", c_uint16),
                ("length", c_uint16),
                ("counter", c_uint32),
                ("j_pos", c_float * 8),
                ("j_speed", c_float * 8),
                ("c_pos", c_float * 6),
                ("c_speed", c_float * 6),
                ("Arm_Angle", c_float),
                ]


def get_status(IP_ADDR="127.0.0.1", PORT=26001):
    list_j_pos = []
    list_c_pos = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Standard socket processes
    payloadS = robot_cmd(1, 8, random.randint(0, 2147483647))  # Fill struct for send with numbers
    s.sendto(payloadS, (IP_ADDR, PORT))  # Default port is 26001
    s.settimeout(3)
    try:
        data, addr = s.recvfrom(1024)  # Need receive return
        payloadR = robot_data.from_buffer_copy(data)
        for i in range(7):
            list_j_pos.append(payloadR.j_pos[i])
        for i in range(6):
            list_c_pos.append(payloadR.c_pos[i])
        return list_j_pos, list_c_pos
    except socket.timeout:
        return False


