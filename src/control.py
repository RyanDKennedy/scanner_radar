from time import sleep
import random

class Control:

    def __init__(self):
        self.yaw = 0
        self.pitch = 0
        self.ready_gpio()


    def ready_gpio(self):
        pass

    def set_yaw(self, yaw):
        self.yaw = yaw
        sleep(0.0002)

    def set_pitch(self, pitch):
        self.pitch = pitch
        sleep(0.0002)

    def get_distance(self):
        return 5 + random.random()
