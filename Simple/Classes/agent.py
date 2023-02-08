import pygame
import numpy as np
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR

start_position = (WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
robot_timestep = 0.1  # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01
INITIAL_ENERGY = 0


class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = SCALE_FACTOR
        self.color = (np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255))
        self.nn = None
        self.genome = None
        self.out_of_bounds = False

    def get_center_coord(self):
        return self.x, self.y

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect

    def move(self, simulation):
        sensed = self.sense(simulation)
        nn_output = self.nn.activate(sensed)
        nn_action = nn_output.index(max(nn_output))

        if nn_action == 0:
            self.x -= SCALE_FACTOR
        elif nn_action == 1:
            self.x += SCALE_FACTOR
        elif nn_action == 2:
            self.y -= SCALE_FACTOR
        elif nn_action == 3:
            self.y += SCALE_FACTOR

        return self.x, self.y

    def sense(self, simulation):
        sensed = []
        #1=NOTHING
        #2=OTHER ROBOT
        #3=FOOD
        robot_coords = set([a.get_center_coord() for a in simulation.population])
        coords_to_check = [(self.x-SCALE_FACTOR, self.y), (self.x+SCALE_FACTOR, self.y), (self.x, self.y-SCALE_FACTOR), (self.x, self.y+SCALE_FACTOR)]

        # for x in range(self.x-SCALE_FACTOR, self.x+SCALE_FACTOR+1, SCALE_FACTOR):
        #     for y in range(self.y-SCALE_FACTOR, self.y+SCALE_FACTOR+1, SCALE_FACTOR):
        for (x, y) in coords_to_check:
            if x == self.x and y == self.y:
                continue
            else:
                if (x, y) in simulation.food:
                    sensed.append(3)
                elif (x, y) in robot_coords:
                    sensed.append(2)
                else:
                    sensed.append(1)
        return sensed





        return sensed


    def simulation_step(self, simulation) -> bool:
        pass

    def simulation_step_rect(self):
        pass

