import amber_api


class Amber_Robot:
    def __init__(self, IP_ADDR, PORT, joint_count):
        self.IP_ADDR = IP_ADDR
        self.PORT = PORT
        self.joint_count = joint_count
        self.joint_upper_limit = [2.0944, 2.0944, 2.0944, 2.0944, 2.0944, 2.0944, 2.0944]
        self.joint_lower_limit = [-2.0944, -2.0944, -2.0944, -2.0944, -2.0944, -2.0944, -2.0944]
        self.DEFAULT_TIMEOUT = 10
        self.DEFAULT_ACCURACY_JOINT = 0.0175
        self.DEFAULT_ACCURACY_CARTESIAN = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05]  # X,Y,Z Roll,Pitch,Yaw

    def move_j(self, j_pos, duration):
        for i in range(7):
            if j_pos[i] > self.joint_upper_limit[i]:
                print(f"Joint {i} exceeds the limit")
                return False
            if j_pos[i] < self.joint_lower_limit[i]:
                print(f"Joint {i} exceeds the limit")
                return False
        # print(f"move: {j_pos} {duration}")
        if amber_api.move_j(j_pos=j_pos, duration=duration, IP_ADDR=self.IP_ADDR, PORT=self.PORT) == 1:
            return True
        else:
            return False

    def move_c(self, c_pos, duration):
        if amber_api.move_c(c_pos=c_pos, duration=duration, IP_ADDR=self.IP_ADDR, PORT=self.PORT) == 1:
            return True
        else:
            return False

    def get_status(self):
        return amber_api.get_status(self.IP_ADDR, self.PORT)

    def gripper_calibrate(self):
        if amber_api.calibrate(actuator_id=8, IP_ADDR=self.IP_ADDR, PORT=self.PORT) == 1:
            return True
        else:
            return False

    def gripper_ctrl(self,action, force):
        if amber_api.gripper_ctrl(action, force,self.IP_ADDR, self.PORT) ==1:
            return True
        else:
            return False


    def set_mode(self, mode):
        if amber_api.set_mode(mode=mode, IP_ADDR=self.IP_ADDR, PORT=self.PORT) == 1:
            return True
        else:
            return False

    def get_mode(self):

        c_mode = amber_api.get_mode(self.IP_ADDR, self.PORT)
        list_mode = []
        for i in range(7):
            list_mode.append(c_mode[i])
        return list_mode

    def set_position_mode(self):
        if amber_api.set_position_mode(self.IP_ADDR, self.PORT, self.joint_count) == 1:
            return True
        else:
            return False

    def set_current_mode(self):
        if amber_api.set_current_mode(self.IP_ADDR, self.PORT, self.joint_count) == 1:
            return True
        else:
            return False

    def wait_for_joint(self, target, timeout=None, accuracy=None):
        if timeout is None: timeout = self.DEFAULT_TIMEOUT
        if accuracy is None: accuracy = self.DEFAULT_ACCURACY_JOINT
        return amber_api.wait_for_joint(target, timeout, accuracy, self.IP_ADDR, self.PORT)

    def wait_for_cartesian(self, target, timeout=None, accuracy=None):
        if timeout is None: timeout = self.DEFAULT_TIMEOUT
        if accuracy is None: accuracy = self.DEFAULT_ACCURACY_CARTESIAN
        if amber_api.wait_for_cartesian(target, timeout, accuracy, self.IP_ADDR, self.PORT) == 1:
            return True
        else:
            return False

    def move_zero(self, duration=3):
        if amber_api.move_j(j_pos=[0, 0, 0, 0, 0, 0, 0], duration=duration, IP_ADDR=self.IP_ADDR, PORT=self.PORT) == 1:
            return True
        else:
            return False



