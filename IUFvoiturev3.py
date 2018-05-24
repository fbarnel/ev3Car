#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from ev3dev.ev3 import *
from tty import *
from sys import *

import termios
import time
import _thread
import threading
import random
import math

def initVariables():
    global vCour, dCour, v0, vMax, vMin
    global direction, roueArriereGauche, roueArriereDroite
    global timeDir, d0, dMax, dMin, ch, dPosCentered
    global dirLock, vLock, backLash, prevDir
    global carLength, carWidth, rapportDir

    v0=0
    vCour=v0
    dPosCentered=70
    vMax=300
    vMin=-300
    timeDir=100
    d0=0
    dCour=0
    ch = 'x'

    roueArriereGauche = LargeMotor('outD')
    roueArriereDroite = LargeMotor('outA')
    direction = MediumMotor('outC')

    dirLock=threading.Lock()
    vLock=threading.Lock()

    carLength=18.5
    carWidth=15
    rapportDir=12*8/(20*24)
    dMax=45/rapportDir
    dMin=-45/rapportDir
    backLash=16/rapportDir
    prevDir=0

def checkPareChoc():
    global vCour, v0
    global direction, roueArriereGauche, roueArriereDroite
    pareChoc = TouchSensor()
    voitureDejaArretee = 0
    while 1:
        if (pareChoc.is_pressed) and ( (not voitureDejaArretee) or vCour>0) :
            dirLock.acquire()
            direction.stop(stop_action='brake')
            dirLock.release()
            vLock.acquire()
            roueArriereGauche.stop(stop_action='brake')
            roueArriereDroite.stop(stop_action='brake')
            vCour=v0
            vLock.release()
            voitureDejaArretee=1
            print("Choc contre obstacle")
            demiTour()

        elif (not pareChoc.is_pressed) and (voitureDejaArretee):
            voitureDejaArretee=0
            print("Obstacle dégagé")

def checkInfraRouge():
    global direction, roueArriereGauche, roueArriereDroite
    global vCour, dCour, v0, vMax, vMin
    global timeDir, d0, dMax, dMin, ch
    global dirLock, vLock


    distanceObstacle=InfraredSensor()

    while ch!='q' :
        if ch!='x' and ch!='s':
            print("Distance obstacle = %d" %(distanceObstacle.value()))
            if distanceObstacle.value()<20 :
                setDirAndSpeed(offsetDir=0, offsetSpeed=-vCour)
                demiTour()
            elif distanceObstacle.value()<40 :
                setDirAndSpeed(offsetDir=0, offsetSpeed=50-vCour)
            elif distanceObstacle.value()<60 :
                if dCour==0 :
                    hasard=random.randint(0,1)
                    if hasard :
                        setDirAndSpeed(offsetDir=20, offsetSpeed=0)
                    else :
                        setDirAndSpeed(offsetDir=-20, offsetSpeed=0)
                else :
                    if dCour > 0 :
                        setDirAndSpeed(offsetDir=20, offsetSpeed=0)
                    else :
                        setDirAndSpeed(offsetDir=-20, offsetSpeed=0)


            elif distanceObstacle.value()>60 :
                setDirAndSpeed(offsetDir=-dCour, offsetSpeed=30)




def InitialisationMecanique():
    global v0, vCour, dPosCentered, dCour
    global direction, roueArriereGauche, roueArriereDroite

    roueArriereGauche.stop(stop_action='brake')
    roueArriereDroite.stop(stop_action='brake')
    vCour=v0

    #direction.speed_sp=-60
    #diffpos=-direction.speed_sp
    #timeDir=250
    #lastDifPos=0
    #BigDifPos=10

    #while BigDifPos>1 or BigDifPos<-1 :
    #    bigLastPos=direction.position
    #    print(bigLastPos)
    #    while (diffpos>1 or diffpos<-1) and lastDifPos*diffpos>=0 :
    #        lastPos=direction.position
    #        direction.run_timed(time_sp=timeDir)
    #        time.sleep(0.2)
    #        currPos=direction.position
    #        lastDifPos=diffpos
    #        diffpos=lastPos-currPos
    #        print(diffpos)
    #    time.sleep(0.5)
    #    bigCurPos=direction.position
    #    print(bigCurPos)
    #    BigDifPos=bigLastPos-bigCurPos


    #direction.run_to_rel_pos(position_sp=dPosCentered)
    #time.sleep(2)
    direction.position=0
    dCour=0

def demiTour() :
    global dCour, vCour, dMin, dMax
    global direction, roueArriereGauche, roueArriereDroite
    global dirLock, vLock

    print("Start demi tour.")

    distRecule=200
    distDemiTour=1000
    offsetDir=0
    offsetGauche=0
    offsetDroite=0

    if dCour>0 :
        offsetDir = 150-dCour
        offsetGauche = distDemiTour
        offsetDroite = -distDemiTour
    else :
        offsetDir = -150-dCour
        offsetGauche = distDemiTour
        offsetDroite = -distDemiTour

    vLock.acquire()
    roueArriereGauche.speed_sp=200
    roueArriereDroite.speed_sp=200
    roueArriereGauche.run_to_rel_pos(position_sp=-distRecule)
    roueArriereDroite.run_to_rel_pos(position_sp=-distRecule)
    vLock.release()

    time.sleep(1)

    dirLock.acquire()
    direction.run_to_rel_pos(position_sp=offsetDir)
    dCour+=offsetDir
    dirLock.release()

    time.sleep(2)

    vLock.acquire()
    roueArriereGauche.speed_sp=200
    roueArriereDroite.speed_sp=200
    roueArriereGauche.run_to_rel_pos(position_sp=offsetGauche)
    roueArriereDroite.run_to_rel_pos(position_sp=offsetDroite)
    vLock.release()

#CHANGE SPEED


def setDirAndSpeed (offsetDir, offsetSpeed ) :
    global dCour, vCour, dMin, dMax
    global direction, roueArriereGauche, roueArriereDroite
    global dirLock, vLock, backLash, prevDir
    global carLength, carWidth, rapportDir

    #print("setDirAndSpeed: offsetDir=%d offsetSpeed=%d" % (offsetDir, offsetSpeed))

    dirLock.acquire()
    if offsetDir!= 0 :
        if (offsetDir>0 and dCour<dMax) or (offsetDir<0 and dCour>dMin) :
            dCour+=offsetDir
            logDir=dCour
            direction.speed_sp=60
            relativePos=offsetDir
            if (offsetDir*prevDir) <= 0 :
                prevDir = offsetDir/abs(offsetDir)
                relativePos += backLash*prevDir
                print("setDirAndSpeed: prevDir=%d, offsetDir=%d, relativePos=%d" %(prevDir, offsetDir, relativePos))
            direction.run_to_rel_pos(position_sp = relativePos)
            dirLock.release()
            print("setDirAndSpeed: tourne %d ec = %d degrés" %(dCour, dCour*rapportDir))
            time.sleep(0.1)
        else :
            logDir=dCour
            dirLock.release()
            print("setDirAndSpeed: tourne déjà au max %d" %dCour)

    if dCour==0 :
        vLock.acquire()
        if offsetSpeed != 0 :
            if (offsetSpeed>0 and vCour<vMax) or (offsetSpeed<0 and vCour>vMin) :
                vCour+=offsetSpeed
                print("setDirAndSpeed: dCour=0 vitesse %d" %vCour)
            else :
                print("setDirAndSpeed: dCour=0 vitesse déjà au max %d" %vCour)
        roueArriereGauche.speed_sp=-vCour
        roueArriereDroite.speed_sp=-vCour
        roueArriereGauche.run_forever()
        roueArriereDroite.run_forever()
        vLock.release()
    else :
        angleRoue=rapportDir*dCour*2*math.pi/direction.count_per_rot
        rayon=carLength/(2*math.sin(angleRoue/2))
        rayonGauche=rayon-(carWidth/2)
        rayonDroit=rayon+(carWidth/2)
        vLock.acquire()
        if offsetSpeed != 0 :
            if (offsetSpeed>0 and vCour<vMax) or (offsetSpeed<0 and vCour>vMin) :
                vCour+=offsetSpeed
                print("setDirAndSpeed: dCour=%d vitesse %d" %(logDir, vCour))
            else :
                print("setDirAndSpeed: dCour=%d vitesse déjà au max %d" %(logDir, vCour))
        if angleRoue>0 :
            roueArriereDroite.speed_sp=-vCour
            roueArriereGauche.speed_sp=-vCour*(rayonGauche/rayonDroit)
        else :
            roueArriereGauche.speed_sp=-vCour
            roueArriereDroite.speed_sp=-vCour*(rayonDroit/rayonGauche)
        roueArriereGauche.run_forever()
        roueArriereDroite.run_forever()
        vLock.release()



def stopAllMotors():
    global direction, roueArriereGauche, roueArriereDroite

    direction.stop(stop_action='brake')
    roueArriereGauche.stop(stop_action='brake')
    roueArriereDroite.stop(stop_action='brake')

    vLock.acquire()
    direction.stop(stop_action='brake')
    roueArriereGauche.stop(stop_action='brake')
    roueArriereDroite.stop(stop_action='brake')
    vCour=v0
    vLock.release()

def checkButton():
    btn = Button()

    while 1:
        if btn.any():
            stopAllMotors()


def commandeClavier():
    global direction, roueArriereGauche, roueArriereDroite
    global vCour, dCour, v0, vMax, vMin
    global timeDir, d0, dMax, dMin, ch
    global dirLock, vLock, rapportDir


    defaultAttr = termios.tcgetattr(stdin.fileno())
    #setraw(stdin.fileno())

    while ch!='q':
        setraw(stdin.fileno())
        ch = stdin.read(1)
        termios.tcsetattr(stdin.fileno(), termios.TCSANOW, defaultAttr)
        if ch == 'a':
            setDirAndSpeed(1/rapportDir,0)
        elif ch == 'd':
            setDirAndSpeed(-1/rapportDir,0)
        elif ch == 'w':
            setDirAndSpeed(0,50)
        elif ch == 's':
            setDirAndSpeed(0,-50)
        elif ch == 'x':
            vLock.acquire()
            dirLock.acquire()
            #InitialisationMecanique()
            stopAllMotors()
            dirLock.release()
            vLock.release()
            print("arret")

    #termios.tcsetattr(stdin.fileno(), termios.TCSANOW, defaultAttr)


def main():
    initVariables()
    #InitialisationMecanique()
    _thread.start_new_thread(checkButton, ())
    _thread.start_new_thread(checkPareChoc, ())
    #_thread.start_new_thread(checkInfraRouge, ())
    commandeClavier()
    stopAllMotors()

main()
