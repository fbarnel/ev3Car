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
             __motor.speed_sp=-100
             #7.61 -> 41
             __motor.run_to_bump( lim_duty_cycle=41, num_int=5, time_out=5000)
             time.sleep(2)
             __motor.position=0
             __motor.position_sp=480
             __motor.speed_sp=200
             __motor.stop_action='brake'
             print("Before Move")

             __motor.run_to_abs_pos()
             time.sleep(3)
             print("After Move")
             time.sleep(3)
             print("After Move2")


             __motor.position=0

        def Set(self, angleRad):


