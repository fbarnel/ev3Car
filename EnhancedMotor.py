#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ev3dev.ev3 import *

import _thread
import threading


class toto:
    def __init__(self):
        print("toto")

    def acquire(self):
        print("acquire")

    def release(self):
        print("release")

class EnhancedMotor(Motor):
    def __init__(self, port):
        super(Motor, self).__init__(port)
        self.__collectingTraces = 0
        self.__motorLock = threading.Lock()

    def run_to_bump(self, lim_duty_cycle=100, num_int=1, time_out=-1):
        num_int_high_pwm=0
        if time_out!=-1 :
            self.run_timed(time_sp=time_out)
            print("movelaunched")
        else:
            self.run_forever()
        while num_int > num_int_high_pwm:
            self.__motorLock.acquire()
            theDutyCycle = abs(self.duty_cycle)
            self.__motorLock.release()
            print("CurrDuutyCycle=%d, limDC=%d, limNumInt=%d, IntHigh=%d" %(theDutyCycle, lim_duty_cycle, num_int, num_int_high_pwm))
            if theDutyCycle > lim_duty_cycle :
                num_int_high_pwm+=1
            else :
                num_int_high_pwm=0
        self.stop(stop_action='coast')
        print("BUMP condition for motor_%s!" %(self.address) )

    def runTraces(self, path="/tmp/dirMotorTraces.txt"):
        fLogTraces=open(path,"w")
        fLogTraces.write("Int\tPWM\tPos\tSpeed\tKPD\tKPP\tKPI\tKSD\tKSP\tKSI\tState\n")
        self.__collectingTraces = 1
        interrupt=0
        while self.__collectingTraces :
            self.__motorLock.acquire()
            theDutyCycle = self.duty_cycle
            self.__motorLock.release()
            fLogTraces.write("%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%d\t%s\n" % (interrupt, theDutyCycle, self.position, self.speed, self.position_d, self.position_p, self.position_i, self.speed_d, self.speed_p, self.speed_i, self.state))
            interrupt+=1
        fLogTraces.close()

    def startTraces(self, dir_for_traces="/tmp"):
        full_path = dir_for_traces + '/' + self.address + "MotorTraces.txt"
        print("full path=%s" %(full_path))
        _thread.start_new_thread(self.runTraces, (full_path, ) )

    def stopTraces(self):
        self.__collectingTraces = 0

class EnhancedMediumMotor(MediumMotor, EnhancedMotor):
    def __init__(self, port):
        super(MediumMotor, self).__init__(port)
        super(EnhancedMotor, self).__init__(port)

class EnhancedLargeMotor(LargeMotor, EnhancedMotor):
    def __init__(self, port):
        super(LargeMotor, self).__init__(port)
        super(EnhancedMotor, self).__init__(port)


