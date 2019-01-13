from EnhancedMotor import *


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

    class Direction:
        def __init__(self, gears, port):
            self.__mech  = MechSystem(gears)
            self.__motor = _EnhancedMediumMotor(port)

        def MechInit():
             self.__backlashDeg     = 16
             self.__maxAngleDeg     = 80
             self.__rotSpeedDegSec  = 40
             self.__bumpSpeedDegSec = 20

             __motor.speed_sp=-(__bumpSpeedDegSec/__mech.getGearTransform())

             #7.61 -> 41
             __motor.run_to_bump( lim_duty_cycle=41, num_int=5, time_out=5000)
             time.sleep(2)
             __motor.position=0
             __motor.position_sp=(__maxAngleDeg + __backlashDeg)/__mech.getGearTransform()
             __motor.speed_sp=__rotSpeedDegSec/__mech.getGearTransform()
             __motor.stop_action='brake'
             __motor.run_to_abs_pos()
             time.sleep(3)

#Use degre as count_per_rot is 360
#Use angleDegre for MechInit constant and count_per_rot
#Use anglrDeg for backlash
             __motor.position=0


        def Set(self, angleDegre):
            if (abs(angleDegre) < __maxAngleDeg) :
                __motor.position_sp = angleDegre/__mech.getGearTransform()
                __motor.speed_sp=__rotSpeedDegSec/__mech.getGearTransform()
                __motor.stop_action='brake'
                __motor.run_to_abs_pos()






