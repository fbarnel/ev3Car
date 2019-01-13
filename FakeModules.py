#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class ev3():
    class Motor():
        def __init__(self, port):
            self.position = 0
            self.spped = 0
            self.position_d = 0
            self.position_p = 0
            self.poition_i = 0
            self.speed_d = 0
            self.speed_p = 0
            self.speed_i = 0
            self.state = ""

        def run_timed(time_sp):
            print("Fake Motor. run_timed.")

        def stop(stop_action):
            print("Fake Motor. stop.")

    class MediumMotor(Motor):
        def __init__(self, port):
            super(Motor, self).__init__(port)

    class LargeMotor(Motor):
        def __init__(self, port):
            super(Motor, self).__init__(port)





