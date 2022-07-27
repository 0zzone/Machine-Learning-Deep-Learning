import numpy as np
import pygame as py
from math import *

from road import Road
from car import Car

from regression import predire

import warnings
warnings.filterwarnings("ignore")

class Env:
    def __init__(self):
        self.road = Road()
        self.car = Car(self.road)
        self.running = True                                                            # used only if u run "world_1" instead of "résau_1"
        self.size = self.weight, self.height = 800, 1000                               # the heigth and weigth of the diplay (not used)
        self.display_surf = py.display.set_mode(self.size, py.HWSURFACE | py.DOUBLEBUF) # the windows


    def step(self): #action is a int
        #the update of the road is made in 'car.update'

        """
        if action ==0:
            alpha = 0 #do noting
        elif action == 1:
            alpha = np.radians(5) #turn right
        elif action == -1:
            alpha = np.radians(-5) #turn left
        """
        #update the car
        #self.car.update(alpha, self.road) #arg the change of delta
        #get captor
        observation = self.car.distance_car_wall(self.road, self.display_surf)
        self.car.update(predire(observation)/50, self.road) #arg the change of delta
        return (observation, self.car.reward, self.car.dead)

    def draw(self):
        #fill blank
        self.display_surf.fill((255, 255, 255))
        #draw the road
        self.road.draw(self.display_surf)
        #draw the car
        self.car.draw(self.display_surf)
        py.display.update()

    def exe_from_env(self):
        clock = py.time.Clock()
        while(self.running):
            clock.tick(30)
            if self.car.dead == False:
                self.car.frame_count +=1
                # print(self.car.frame_count)
            else:
                self.car.get_fitness()
            action = 0

            for event in py.event.get():
                if event.type == py.QUIT:
                    self.running = False
                """
                if event.type == py.KEYDOWN:
                    if (event.key == py.K_RIGHT):
                        action = 1
                    if (event.key == py.K_LEFT):
                        action = -1
                """


            #draw
            self.draw()
            self.step()


if __name__ == "__main__" :
    env = Env()
    env.exe_from_env()
