from EnhancedMotor import *
import time


class Car:
    #Sait faire:
    #Aller tout droit, v constante, accel, decel
    #suivre une courbe: Rmin et Rmax?
    #connaitre sa position (par rapport a position initiale)
    #memoriser trajectoires
    #detecter obstacles
    #caractériser obstacles
    #mémoriser position obstracles
    #eviter les obstacles nouveaux et déjà mémorisés

    #Attributs:
    #Liste systemes mecaniques
    #Position-orientation(x, y, t(angle theta)), vitesse(dx, dy, dt), acceleration(ddx, ddy, ddt)

    #A faire:
    #traduire trajectoire en contraintes sur positions/vitesse, acceleration
    #traduire position/vitesse/accel en contraintes sur liste systemes mecaniques.

    class DirectionModule:
        def __init__(self, gears, port, propEvent, dirEvent):
            self.__mech         = MechSystem(gears)
            self.__motor        = EnhancedMediumMotor(port)
            self.__propEvent    = propEvent
            self.__dirEvent     = dirEvent

        def MechInit():
             #All angles are in degres and speeds in degres per second
             #This shall be read from a config file.
             self.__backlashDeg     = 16
             self.__maxAngleDeg     = 80
             self.__rotSpeedDegSec  = 40
             self.__bumpSpeedDegSec = 20
             self.__stabilizeDelay  = 3
             self.__numIntBump      = 5

             __motor.speed_sp=-(__bumpSpeedDegSec/__mech.getGearTransform())

             """ There is a need to buiuld a database:
                 Voltage -> lim_duty_cycle for bump
                 7.61    -> 41
             """

             __motor.run_to_bump( lim_duty_cycle=41, num_int=__numIntBump, time_out=5000)
             time.sleep(__stabilizeDelay)
             __motor.position=0
             __motor.position_sp=(__maxAngleDeg + __backlashDeg)/__mech.getGearTransform()
             __motor.speed_sp=__rotSpeedDegSec/__mech.getGearTransform()
             __motor.stop_action='brake'
             __motor.run_to_abs_pos()
             time.sleep(__stabilizeDelay)

#Use degre as count_per_rot is 360
#Use angleDegre for MechInit constant and count_per_rot
#Use anglrDeg for backlash
             __motor.position=0


        #Set direction at a specific angle in degres
        def Set(self, angleDegre):

            #Check that last wheels speed update of power module is finished
            __propEvent.wait()

            if (abs(angleDegre) < __maxAngleDeg ) :
                __motor.position_sp = angleDegre/__mech.getGearTransform()
                __motor.speed_sp=__rotSpeedDegSec/__mech.getGearTransform()
                __motor.stop_action='brake'
                __motor.run_to_abs_pos()

                #Advise power module to compute and update wheels speed
                __propEvent.set()

        def Stop(self):
             __motor.stop_action='brake'


    class PropulsionModule:
        def __init__(self, numActautors, gears, port, distActuation, powerEvent, dirEvent):
            #Check coherency of parameters
            if (gears.size() != numActuators) :
                print("ERROR: number Gears systems = %d and numActuators = %d " %(gears.size(), numActuators))
                return
            if (port.size() != numActuators) :
                print("ERROR: number of ports = %d and numActuators = %d " %(port.size(), numActuators))
                return
            if (gears.size() != numActuators) :
                print("ERROR: number distance passed = %d and numActuators=%d " %(distActuation.size(), numActuators))
                return

            #A propulsion module can be made of several actuators
            for index in range(numActuators):
                self.__mech[index]  = MechSystem(gears[index])
                self.__motor[index] = EnhancedMediumMotor(port[index])
                self.__distA[index] = distActuation[index]

            self.__propEvent    = propEvent
            self.__dirEvent     = dirEvent

        def MechInit():
             #All angles are in degres and speeds in degres per second
             self.__backlashDeg     = 16




