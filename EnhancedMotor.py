#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ev3dev.ev3 import *

import _thread
import threading
import pickle
import math

class EnhancedMotor(Motor):
    def __init__(self, port):
        super(Motor, self).__init__(port)
        self.__collectingTraces = 0
        self.__motorLock = threading.Lock()
        self.__tracesLock = threading.Lock()
        self.__traceFileNum = 0
        self.__basePath = ''

    dataTrace = {
        'interrupt' : 0,
        'PWM' : 0,
        'Pos' : 0,
        'Speed' : 0,
        'KPD' : 0,
        'KPP' : 0,
        'KPI' : 0,
        'KSD' : 0,
        'KSP' : 0,
        'KSI' : 0,
        'State' : 'hold'
    }


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
            print("Current duty cycle=%d, limDC=%d, limNumInt=%d, IntHigh=%d" %(theDutyCycle, lim_duty_cycle, num_int, num_int_high_pwm))
            if theDutyCycle > lim_duty_cycle :
                num_int_high_pwm+=1
            else :
                num_int_high_pwm=0
        self.stop(stop_action='coast')
        print("BUMP condition for motor_%s!" %(self.address) )

    def runTraces(self):
        self.__tracesLock.acquire()
        self.__collectingTraces = 1
        interrupt = 0
        listTrace = []
        fullPath = self.__basePath + str(self.__traceFileNum) + '.bin'
        fLogTraces = open(fullPath,'wb')
        while self.__collectingTraces :
            print("traces enabled in while=%d" %self.__collectingTraces)
            self.__motorLock.acquire()
            theDutyCycle = self.duty_cycle
            self.__motorLock.release()
            self.dataTrace = (interrupt, theDutyCycle, self.position, self.speed, self.position_d, self.position_p, self.position_i, self.speed_d, self.speed_p, self.speed_i, self.state)
            listTrace.append(dataTrace)
            interrupt+=1
            if not interrupt%2000:
                pickle.dump(listTrace, fLogTraces, pickle.DEFAULT_PROTOCOL)
                fLogTraces.close()
                self.__traceFileNum+=1
                fullPath = path + str(self.__traceFileNum) + '.bin'
                fLogTraces = open(fullPath,'wb')

        if interrupt%2000:
            pickle.dump(listTrace, fLogTraces, pickle.DEFAULT_PROTOCOL)
            self.__traceFileNum+=1

        fLogTraces.close()
        self.__tracesLock.release()

    def startTraces(self, dir_for_traces='/tmp'):
        self.__basePath = dir_for_traces + '/' + self.address + 'MotorTraces'
        print("base path=%s" %(self.__basePath))
        _thread.start_new_thread(self.runTraces, () )

    def stopTraces(self):
        self.__collectingTraces = 0
        print("traces enabled in stopTraces=%d" %self.__collectingTraces)
        self.__tracesLock.acquire()
        self.__tracesToTxt()
        self.__traceFileNum = 0
        self.__tracesLock.release()

    def __tracesToTxt(self):
        pathTxt = self.__basePath+'.txt'
        with open(path, 'w') as fLogTracesTxt:
            fLogTracesTxt.write("Int\tPWM\tPos\tSpeed\tKPD\tKPP\tKPI\tKSD\tKSP\tKSI\tState\n")
            for fileNum in range(self.__traceFileNum):
                pathBin = self.__basePath+str(fileNum)+'.bin'
                with open(path, 'rb') as fLogTracesBin:
                    data = pickle.load(fLogTracesBin)

                    for dataTrace in data:
                        fLogTracesTxt.write(dataTrace)

                fLogTracesBin.close()
        fLogTracesTxt.close()


#When transformation is linear, gear teeth represents number of teeth to advance 1m
#When transformation is a rotation, gear teeth represents number of teeth to turn 360 degrees
gearDescr = {
        'sameAxis'  : 1,
        'toLinear'  : 1,
        'gearTeeth' : math.pi*0.07
}

gearDescr0={'sameAxis': 1, 'toLinear': 0, 'gearTeeth':12}
gearDescr1={'sameAxis': 0, 'toLinear': 0, 'gearTeeth':20}
gearDescr2={'sameAxis': 1, 'toLinear': 0, 'gearTeeth':8}
gearDescr3={'sameAxis': 0, 'toLinear': 0, 'gearTeeth':24}
listGearsDir=[gearDescr0,gearDescr1,gearDescr2,gearDescr3]




class MechSystem():
    def __init__(self, gears):
        self.__gears = gears
    def getType(self):
        if self.__gears[-1]['toLinear'] :
            return 'Linear'
        else :
            return 'Rotation'

    #When transformation type is linear this methods return number of meter per motor rotation
    #When transformation type is rotation this methods return number of rotation per motor rotation
    def getGearTransform(self):
        transform=1
        for gearDescr in self.__gears:
            if gearDescr['sameAxis'] :
                transform *= gearDescr['gearTeeth']
            else :
                transform /= (-gearDescr['gearTeeth'])
        return transform

    #TBD define moves, turn, distance speed using transform. Necessary?


class EnhancedMediumMotor(MediumMotor, EnhancedMotor):
    def __init__(self, port):
        super(MediumMotor, self).__init__(port)
        super(EnhancedMotor, self).__init__(port)

class EnhancedLargeMotor(LargeMotor, EnhancedMotor):
    def __init__(self, port):
        super(LargeMotor, self).__init__(port)
        super(EnhancedMotor, self).__init__(port)

