from time import sleep
import random

import RPi.GPIO as GPIO

class Control:

    def __init__(self, yaw_deg_per_step, pitch_deg_per_step):
        self.yaw = 0
        self.pitch = 0
        self.yaw_deg_per_step = yaw_deg_per_step
        self.pitch_deg_per_step = pitch_deg_per_step

        self.step_yaw_pin = 23
        self.dir_yaw_pin = 24

        self.step_pitch_pin = 27
        self.dir_pitch_pin = 22
        
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.step_yaw_pin, GPIO.OUT)
        GPIO.setup(self.dir_yaw_pin, GPIO.OUT)
        GPIO.setup(self.step_pitch_pin, GPIO.OUT)
        GPIO.setup(self.dir_pitch_pin, GPIO.OUT)
        
        GPIO.output(self.step_yaw_pin, GPIO.LOW)
        GPIO.output(self.dir_yaw_pin, GPIO.LOW)
        GPIO.output(self.step_pitch_pin, GPIO.LOW)
        GPIO.output(self.dir_pitch_pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

    def set_yaw(self, desired_yaw):
        clockwise = GPIO.LOW
        counter_clockwise = GPIO.HIGH

        # calculate steps
        dtheta = desired_yaw - self.yaw
        steps = round(abs(dtheta / self.yaw_deg_per_step))

        # get direction and new self.yaw
        direction = clockwise
        if (dtheta < 0):
            direction = counter_clockwise
            self.yaw -= steps * self.yaw_deg_per_step
        else:
            direction = clockwise
            self.yaw += steps * self.yaw_deg_per_step

        # do gpio stuff
        delay = 0.1
        GPIO.output(self.dir_yaw_pin, direction)
        sleep(delay)
        for step_num in range(0, steps):
            GPIO.output(self.step_yaw_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_yaw_pin, GPIO.LOW)
            sleep(delay)

    def set_pitch(self, desired_pitch):
        up = GPIO.LOW
        down = GPIO.HIGH

        # calculate steps
        dtheta = desired_pitch - self.pitch
        steps = round(abs(dtheta / self.pitch_deg_per_step))

        # get direction and new self.pitch
        direction = up
        if (dtheta < 0):
            direction = down
            self.pitch -= steps * self.pitch_deg_per_step
        else:
            direction = up
            self.pitch += steps * self.pitch_deg_per_step

        # do gpio stuff
        delay = 0.005
        GPIO.output(self.dir_pitch_pin, direction)
        sleep(delay)
        for step_num in range(0, steps):
            GPIO.output(self.step_pitch_pin, GPIO.HIGH)
            sleep(delay)
            GPIO.output(self.step_pitch_pin, GPIO.LOW)
            sleep(delay)

    def get_distance(self):
        return 5 + random.random()
