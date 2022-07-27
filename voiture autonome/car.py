from dis import dis
import pygame as py
import numpy as np
from math import *

BLACK = (0, 0, 0)

vec2 = py.math.Vector2

class Car:
    heigth = 40
    width = 20
    focal = 600
    frame_count = 0
    fitness = 0
    acceleration_max = 5
    minim_safe_dist = 2/focal

    def __init__ (self, road):
        self.reward
        self.capteur = [0] * 5
        self.direction = 0 #used a lot
        self.vitesse = vec2(0, -3).rotate_rad(self.direction) #not used for the moment
        self.dead = False
        self.position_centre = py.math.Vector2(road.where_x(550), 550) #the position of the center
        self.position_par_rapport_centre = [None] * 4    #of the 4 angles relative to the center
        self.position_calcul()

#------------------------------------fonction appelé par l'extérieur-------------------------

    #function of update of the position of the car given an delta
    def update(self, delta, road):
        #given a delta to add to the direction add it
        self.direction = (self.direction + delta) % (2*pi)  # needs to stay between 0 and 2pi
        #update vitesse
        self.vitesse = self.vitesse.rotate_rad(delta)
        y_before = self.position_centre.y
        if not(self.dead):
            road.update(-self.vitesse.y)
            #for the moment the car donc have to know where it needs to be
            self.position_centre.x += self.vitesse.x

        self.reward = -self.vitesse.y
        #update with the new direction the position of the angle of the car (same method as in the begining)
        self.position_calcul()


    """------------------------------------------------------------------------------------------"""
    def draw(self, display):
        #to draw the car (a simple polygone)
        points = []
        for i in range (4):
            points.append (self.position_centre+ self.position_par_rapport_centre[i])

        py.draw.polygon(display, BLACK, points, 3)

        #la boussole de la voiture (celle à droite)
        dir = to_pi(self.direction)
        x = py.math.Vector2(0, -50).rotate_rad(dir)
        py.draw.line(display, (1, 1, 1),py.math.Vector2(300, 900)+x, (300, 900), 2)
        py.draw.circle(display, (1, 1, 1), (300, 900), 70, 3)

    """------------------------------------------------------------------------------------------"""

    #input : himself and a display where the road is drawn
    #output : return a tab of input for the NN and if the car is dead
    def distance_car_wall(self, road, display):
        capt = [] #the tab that will be returned

        for i in range (4):
            #all this mess is just to call the function "captor find" with the good position and angle
            if i <= 1:
                # see the explaination of captor find
                # others x are the same
                x = self.captorfind(road, (self.direction-(pi/4)+(pi/2)*i), self.position_centre+self.position_par_rapport_centre[i], display)
            else:
                if i == 2:
                    x_y = py.math.Vector2(-self.width/2, 0).rotate_rad(self.direction)
                elif i == 3:
                    x_y = py.math.Vector2(self.width/2, 0).rotate_rad(self.direction)

                x = self.captorfind(road, (self.direction+(pi)*i-(5*pi/2)), self.position_centre + x_y, display)


            if x <= self.minim_safe_dist:
                self.dead = True

            capt.append(x)
        return capt

    def reward(self):
        return self.reward

#--------------------------------fonction interne----------------------------------

    # input : the car, a display, a direction to search and an initial position
    # output : the first (1, 1, 1) pixel in the direction given form the initial position
    # metod : go check every pixel in a certain range and return the first one that is black, the range else
    def captorfind(self, road, orientation, position, display):
        i = 0               #acc for the distance
        x = position.x      #variable of position which will evolue
        y = position.y

        minDist = self.focal
        Dir = position + vec2(0,-self.focal).rotate_rad(orientation)
        x_y = vec2(int(Dir.x), int(Dir.y))
        #sur tout les segments de la route...
        for i in range (road.nbr_segment_for_the_road * road.nbr_sub_segmentation - 1):
            #collision avec la gauche de la route
            collisionPoint = getCollisionPoint(road.point_g[i].x, road.point_g[i].y, road.point_g[i+1].x, road.point_g[i+1].y, position.x, position.y, Dir.x, Dir.y)
            if collisionPoint is None:
                pass
            else:
                #la longueur entre le point de départ du capteur et l'intersection
                length = py.math.Vector2.length(vec2(int(collisionPoint.x - position.x), int(collisionPoint.y - position.y)))
                if length < minDist:
                    minDist = length
                    x_y = vec2(int(collisionPoint.x), int(collisionPoint.y))
            #collision avec la droite de la route
            collisionPoint = getCollisionPoint(road.point_d[i].x, road.point_d[i].y, road.point_d[i+1].x, road.point_d[i+1].y, position.x, position.y, Dir.x, Dir.y)
            if collisionPoint is None:
                continue #finie l'ittération de for pour pas faire de calcul supplémentaire inutile
            else:
                length = py.math.Vector2.length(vec2(int(collisionPoint.x - position.x), int(collisionPoint.y - position.y)))
                if length < minDist:
                    minDist = length
                    x_y = vec2(int(collisionPoint.x), int(collisionPoint.y))

        py.draw.circle( display, ( 0,0, 200 ), x_y, 4 )     #a circle at the colision
        py.draw.line( display, BLACK, position, x_y, 2 )

        return minDist/self.focal


    def position_calcul(self):
        for i in range (4):
            x = int(self.width/2) * ((-1)**(((i+1)//(2))+1))   # just to hav - + + -
            y = int(self.heigth/2) * ((-1)**((i//2)+1))        # bis but + + - -
            x_y = py.math.Vector2(x, y).rotate_rad(self.direction)
            self.position_par_rapport_centre[i] = x_y

    #no used for the moment but in theorie should work
    def is_dead(self):
        pass
        """todo"""
        #x_y = self.position_centre+ (py.math.Vector2(self.height/2, 0).rotate_rad(self.direction))
        #return (self.captorfind(display, x_y , self.direction) > self.vitesse)

    def get_fitness(self):
        self.fitness = 1-(1/(log(self.frame_count)+1))
        print(self.fitness)

#----------------------------------------fonction auxilière------------------------------

#map an alpha from [0, 2pi] to [-pi, pi]
def to_pi(x):
    return (x+pi)%(2*pi)-pi

#la collision entre deux vecteurs
def getCollisionPoint(x1, y1, x2, y2, x3, y3, x4, y4):
    uA = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    uB = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))
    if 0 <= uA <= 1 and 0 <= uB <= 1:
        intersectionX = x1 + (uA * (x2 - x1))
        intersectionY = y1 + (uA * (y2 - y1))
        return vec2(intersectionX, intersectionY)
    return None
