import time
from amber_api import basic_cmd

DEFAULT_TIMEOUT = 10
DEFAULT_ACCURACY_JOINT = 0.0175  # rad, for every joint, 0.0175 rad= 1 degree
DEFAULT_ACCURACY_CARTESIAN = 0.001


def wait_for_mode(expected, timeout, joint_count=7, IP_ADDR="127.0.0.1", PORT=26001):
    use_time = 0
    while True:
        result = basic_cmd.cmd_110.get_mode(IP_ADDR=IP_ADDR, PORT=PORT)
        print(result[0], )
        passed = 0
        for i in range(joint_count):
            if result[i] == expected:
                passed += 1
        if passed == joint_count:
            return True
        else:
            use_time += 0.1
            time.sleep(0.1)
            if use_time > timeout:
                return False


def set_active_mode(IP_ADDR="127.0.0.1", PORT=26001):
    basic_cmd.set_mode(mode=1, IP_ADDR=IP_ADDR, PORT=PORT)


def set_position_mode(IP_ADDR="127.0.0.1", PORT=26001,joint_count=7):
    set_active_mode(IP_ADDR=IP_ADDR, PORT=PORT)
    wait_for_mode(1, 1, joint_count=joint_count, IP_ADDR=IP_ADDR, PORT=PORT)
    basic_cmd.set_mode(mode=2, IP_ADDR=IP_ADDR, PORT=PORT)


def set_current_mode(IP_ADDR="127.0.0.1", PORT=26001,joint_count=7):
    set_active_mode(IP_ADDR=IP_ADDR, PORT=PORT)
    wait_for_mode(1, 1, joint_count=joint_count, IP_ADDR=IP_ADDR, PORT=PORT)
    basic_cmd.set_mode(mode=4, IP_ADDR=IP_ADDR, PORT=PORT)


def wait_for_joint(target, timeout=DEFAULT_TIMEOUT, accuracy=DEFAULT_ACCURACY_JOINT, IP_ADDR="127.0.0.1", PORT=26001,
                   actuator_count=7):
    delta_flag = [0, 0, 0, 0, 0, 0, 0, 0]
    use_time = 0
    while True:
        delta_all = 0
        now_j, now_c = basic_cmd.cmd_1.get_status(IP_ADDR=IP_ADDR, PORT=PORT)
        for i in range(7):
            delta = abs(now_j[i] - target[i])
            delta_all += delta
            # print(delta)
            if delta < accuracy:
                delta_flag[i] = 1
            else:
                delta_flag[i] = 0
        flag = 0
        for i in range(8):
            flag += delta_flag[i]
        if flag > actuator_count - 1:
            return True

        time.sleep(0.1)
        use_time += 0.1
        if use_time > timeout:
            return False


def wait_for_cartesian(target, timeout=DEFAULT_TIMEOUT, accuracy=DEFAULT_ACCURACY_CARTESIAN, IP_ADDR="127.0.0.1",
                       PORT=26001):
    delta_flag = [0, 0, 0, 0, 0, 0]
    use_time = 0
    while True:
        delta_all = 0
        now_j, now_c = basic_cmd.cmd_1.get_status(IP_ADDR=IP_ADDR, PORT=PORT)
        for i in range(6):
            delta = abs(now_c[i] - target[i])
            delta_all += delta
            # print(delta)
            if delta < accuracy[i]:
                delta_flag[i] = 1
            else:
                delta_flag[i] = 0
        flag = 0
        for i in range(6):
            flag += delta_flag[i]
        if flag > 5:
            return True

        time.sleep(0.1)
        use_time += 0.1
        if use_time > timeout:
            return False
