import pygame
import numpy as np
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR

start_position = (WORLD_WIDTH / 2, WORLD_HEIGHT / 2)
robot_timestep = 0.1  # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01
INITIAL_ENERGY = 0
SENSING_DISTANCE = 8


class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = SCALE_FACTOR
        self.color = (np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255))
        self.sensing_rects = []
        self.nn = None
        self.genome = None
        self.out_of_bounds = False
        self.previous_locations = [(self.x, self.y)]

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
        amount_of_food_north = 0
        amount_of_food_east = 0
        amount_of_food_south = 0
        amount_of_food_west = 0
        distance_to_edge_north = SENSING_DISTANCE
        distance_to_edge_east = SENSING_DISTANCE
        distance_to_edge_south = SENSING_DISTANCE
        distance_to_edge_west = SENSING_DISTANCE
        distance_to_robot_north = SENSING_DISTANCE
        distance_to_robot_east = SENSING_DISTANCE
        distance_to_robot_south = SENSING_DISTANCE
        distance_to_robot_west = SENSING_DISTANCE


        # amount_of_robots_north = 0
        # amount_of_robots_east = 0
        # amount_of_robots_south = 0
        # amount_of_robots_west = 0

        robot_coords = set([a.get_center_coord() for a in simulation.population])
        self.sensing_rects = []
        #NORTH
        for i in range(SENSING_DISTANCE+1):
            coord = self.x, self.y-i*SCALE_FACTOR
            self.sensing_rects.append(coord)
            if coord in simulation.food:
                amount_of_food_north += 1
            elif coord[1] < 0 and distance_to_edge_north == SENSING_DISTANCE:
                distance_to_edge_north = i-1
            elif coord in robot_coords and distance_to_robot_north == SENSING_DISTANCE:
                distance_to_robot_north = i-1
                #amount_of_robots_north += 1

        #EAST
        for i in range(SENSING_DISTANCE+1):
            coord = self.x + i*SCALE_FACTOR, self.y
            self.sensing_rects.append(coord)
            if coord in simulation.food:
                amount_of_food_east += 1
            elif coord[0] > WORLD_WIDTH and distance_to_edge_east == SENSING_DISTANCE:
                distance_to_edge_east = i-1
            elif coord in robot_coords and distance_to_robot_east:
                distance_to_robot_east = i-1
                #amount_of_robots_east += 1

        #SOUTH
        for i in range(SENSING_DISTANCE+1):
            coord = self.x, self.y + i *SCALE_FACTOR
            self.sensing_rects.append(coord)
            if coord in simulation.food:
                amount_of_food_south += 1
            elif coord[1] > WORLD_HEIGHT and distance_to_edge_south == SENSING_DISTANCE:
                distance_to_edge_south = i-1
            elif coord in robot_coords and distance_to_robot_south == SENSING_DISTANCE:
                distance_to_robot_south = i-1
                #amount_of_robots_south += 1


        #WEST
        for i in range(SENSING_DISTANCE+1):
            coord = self.x - i*SCALE_FACTOR, self.y
            self.sensing_rects.append(coord)
            if coord in simulation.food:
                amount_of_food_west += 1
            elif coord[0] < 0 and distance_to_edge_west == SENSING_DISTANCE:
                distance_to_edge_west = i-1
            elif coord in robot_coords and distance_to_robot_west == SENSING_DISTANCE:
                distance_to_robot_west = i-1
                #amount_of_robots_west += 1


        return [amount_of_food_north/SENSING_DISTANCE, amount_of_food_east/SENSING_DISTANCE, amount_of_food_south/SENSING_DISTANCE, amount_of_food_west/SENSING_DISTANCE,
                distance_to_edge_north/SENSING_DISTANCE, distance_to_edge_east/SENSING_DISTANCE, distance_to_edge_south/SENSING_DISTANCE, distance_to_edge_west/SENSING_DISTANCE,
                distance_to_robot_north/SENSING_DISTANCE, distance_to_robot_east/SENSING_DISTANCE, distance_to_robot_south/SENSING_DISTANCE, distance_to_robot_west/SENSING_DISTANCE
                #amount_of_robots_north, amount_of_robots_east, amount_of_robots_south, amount_of_robots_west
                ]



    def simulation_step(self, simulation) -> bool:
        pass

    def simulation_step_rect(self):
        pass

