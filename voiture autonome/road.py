from scipy import interpolate
from scipy.misc import derivative
import pygame as py
import numpy as np
from math import *
import random

BLACK = (1, 1, 1)
GREY = (1, 1, 1)

vec2 = py.math.Vector2

class Road:

    nbr_segment_for_the_road = 5#3 #need some adjustment for it to be changeable
    nbr_sub_segmentation = 10
    width_road = 65
    possible_x_ecart = 70

    def __init__(self):
        # initialize a conteur of how much did the road go down by
        self.decalage = 0
        #initialize les points de repère pour la route
        self.repere_points = [((vec2(300, -250)), self.width_road)]
        for i in range (2):
            self.repere_points.append((vec2(random_in_interval(self.repere_points[i-1][0].x , 100, 500, self.possible_x_ecart), (-250 * i - 500)), self.width_road))

        # initialization of useful things :
        # the interpolation function between repere_points
        self.tab_of_function = []
        # the tab which contain all points used to draw the road
        self.tab_of_all_points = []
        self.point_g = []
        self.point_d = []
        # the methode of construction and update is spetial, a text is hard to explain
        for i in range (self.nbr_segment_for_the_road):
            for j in range (len(self.repere_points)):
                self.repere_points[j][0].y += 250 ### same
            self.repere_points.append((vec2(random_in_interval(self.repere_points[i-1][0].x, 100, 500, self.possible_x_ecart), (-750)), self.width_road))
            self.update_function(i)
            for j in range (len(self.tab_of_all_points)):
                self.tab_of_all_points[j].y += 250
                self.point_g[j].y += 250
                self.point_d[j].y += 250
            self.update_points(i)

#------------------------------------fonction appelé par l'extérieur------------------

    # update all thing in rapport with the road
    def update (self, dx):
        # update points positions
        for i in range (self.nbr_segment_for_the_road * self.nbr_sub_segmentation + 1):
            self.tab_of_all_points[i].y += dx
            self.point_g[i].y += dx
            self.point_d[i].y += dx
        self.decalage += dx

        # check si le dernier points n'est pas trop en bas
        self.check_update_if_rp_depassed()

    """------------------------------------------------------------------------------------------"""

    def draw(self, display): # dessiner la route et tout le nécessaire

        for i in range (0, self.nbr_segment_for_the_road * self.nbr_sub_segmentation + 1):
            if i < self.nbr_segment_for_the_road * self.nbr_sub_segmentation:
                #trace les bords de routes
                py.draw.line(display, BLACK, self.point_g[i], self.point_g[i+1], 3)
                py.draw.line(display, BLACK, self.point_d[i], self.point_d[i+1], 3)


        #draw the square
        py.draw.line(display, BLACK, (50, 0), (50, 750), 3)
        py.draw.line(display, BLACK, (50, 750), (550, 750), 3)
        py.draw.line(display, BLACK, (550, 750), (550, 0), 3)

        # hide the line at the bottom of the square
        py.draw.rect(display, (255, 255, 255), ((50, 750), (500, 300)))
        # hide at the right of the square
        py.draw.rect(display, (255, 255, 255), ((550, 0), (200, 1000)))
        # hide at the left of the square
        py.draw.rect(display, (255, 255, 255), ((0, 0), (50, 1000)))

        #la boussole de la route (celle à gauche)
        alp = self.what_is_delta(650)
        x = py.math.Vector2(0, -50).rotate_rad(alp)
        py.draw.line(display, (1, 1, 1),py.math.Vector2(100, 900) + x, (100, 900), 2)
        py.draw.circle(display, (1, 1, 1), (100, 900), 70, 3)

    """------------------------------------------------------------------------------------------"""

    # retourne la valeur de la la fonction (donc du centre de la route) en fonction du y
    def where_x(self, pos_y):
        pos_y -= self.decalage
        i = 2-int(pos_y//250)
        y = (pos_y % 250) - 500 ###
        return self.tab_of_function[i](y)

    # retourne la valeur de la tangente en y
    def what_is_delta(self, pos_y):
        pos_y -= self.decalage
        i = 2-int(pos_y//250)
        y = (pos_y % 250) -500
        return -np.arctan(derivative(self.tab_of_function[i],y))

#--------------------------------fonction interne----------------------------------

    # when called update the function of indice given (the indice give where the road is)
    def update_function(self, indice):
        # x are f(x) given to the interpolations
        x = [
            self.repere_points[indice    ][0].x, ### le [0] est pour la gestion des tuples
            self.repere_points[indice + 1][0].x,
            0,
            self.repere_points[indice + 2][0].x,
            0,
            self.repere_points[indice + 3][0].x
        ]
        # y are x value in f(x) for the interpolation
        y = [
            self.repere_points[indice    ][0].y,
            self.repere_points[indice + 1][0].y,
            self.repere_points[indice + 1][0].y,
            self.repere_points[indice + 2][0].y,
            self.repere_points[indice + 2][0].y,
            self.repere_points[indice + 3][0].y
        ]
        # so (y , x) is [x1, x2, ...] [f(x1), f(x2), ...]
        # add the function at the end of the tab of function
        self.tab_of_function.append(interpolate.KroghInterpolator(y, x))


    # tu lui donne un indice et la fonction te rajoute les points pour la fonction de l'indice
    def update_points(self, indice):
        if indice != 0:
            self.tab_of_all_points.pop()
            self.point_g.pop()
            self.point_d.pop()
        delta1 = self.repere_points[indice + 2][1]
        delta2 = self.repere_points[indice + 3][1]
        f = interpolate.interp1d((self.repere_points[indice + 2][0].y, self.repere_points[indice + 3][0].y), (delta1, delta2))
        for i in range (self.nbr_sub_segmentation + 1):
            y = -(250 / self.nbr_sub_segmentation) * i + self.repere_points[indice + 1][0].y
            x = int(self.tab_of_function[indice](y))
            alpha = -np.arctan(derivative(self.tab_of_function[indice],y))

            self.tab_of_all_points.append(vec2(x, y))
            left_size = -f(y - 250)
            rigth_size = f(y - 250)
            self.point_g.append(vec2(x, y) + vec2(left_size, 0).rotate_rad(alpha))
            self.point_d.append(vec2(x, y) + vec2(rigth_size, 0).rotate_rad(alpha))


    # update les points quand ils sont trop bas
    def check_update_if_rp_depassed(self):
        if self.decalage > 250:
            # enleve la fonction 0 de la list
            self.tab_of_function.pop(0)
            # enlève tout les points inutile (pour en remettre à la fin juste après)
            for i in range (self.nbr_sub_segmentation):
                self.tab_of_all_points.pop(0)
                self.point_g.pop(0)
                self.point_d.pop(0)
            # ...
            self.repere_points.pop(0)

            for i in range(self.nbr_segment_for_the_road + 2):
                self.repere_points[i][0].y += 250

            self.repere_points.append((vec2(random_in_interval (self.repere_points[self.nbr_segment_for_the_road - 2][0].x, 100, 500, self.possible_x_ecart), -750), self.width_road))
            # remet une nouvelle fonction à la fin de la list
            self.update_function(self.nbr_segment_for_the_road - 1)
            self.update_points(self.nbr_segment_for_the_road - 1)
            self.decalage = 0


#----------------------------------------fonction auxilière------------------------------

# input : a number between 0 and 2pi
# ouput : a number between -pi and pi
# all number over pi are transformed into negative one
def to_pi(x):
    return (x+pi)%(2*pi)-pi

# ouput : a number random between the min and the max while also being in [x-delta, x+delta]
def random_in_interval(x_before, left, right, delta):
    return random.randint(max(left, x_before-delta), min(right, x_before+delta))
