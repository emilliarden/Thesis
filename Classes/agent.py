import pygame
import neat
import queue
from Classes.constants import Constants, SensingMode, ContentOfSquare
from enum import Enum


class Agent:
    def __init__(self, genome, config, constants):
        self.constants = constants
        self.x = constants.START_POSITION[0]
        self.y = constants.START_POSITION[1]
        self.size = constants.SCALE_FACTOR
        self.color = (200, 8, 8)
        self.sensing_distance = constants.SENSING_DISTANCE
        self.sensing_rects = []
        self.previous_positions = queue.Queue(10)
        self.genome = genome
        self.nn = neat.nn.RecurrentNetwork.create(genome, config)
        self.out_of_bounds = False
        self.timesteps_without_progress = 0
        self.timesteps_alive = 0
        self.sensing_mode = constants.SENSING_MODE
        self.energy = self.constants.ALLOWED_MOVES_WITHOUT_PROGRESS
        self.last_nn_output = [0, 0, 0, 0]

    def get_center_coord(self):
        return self.x, self.y

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect

    def move(self, simulation):
        if self.previous_positions.full():
            self.previous_positions.get()
        self.previous_positions.put((self.x, self.y))

        if self.sensing_mode == SensingMode.Pyramid:
            sensed = self.sense_pyramid(simulation)
        elif self.sensing_mode == SensingMode.Box:
            sensed = self.sense_box(simulation)
        elif self.sensing_mode == SensingMode.Cross:
            sensed = self.sense_cross(simulation)
        elif self.sensing_mode == SensingMode.BoxDiff:
            sensed = self.sense_boxDiff(simulation)

        sensed.append(self.x/self.constants.WORLD_WIDTH)
        sensed.append(self.y/self.constants.WORLD_HEIGHT)
        sensed.append(self.timesteps_without_progress / self.constants.ALLOWED_MOVES_WITHOUT_PROGRESS)

        nn_output = self.nn.activate(sensed + self.last_nn_output)
        self.last_nn_output = nn_output

        nn_action = nn_output.index(max(nn_output))

        if nn_action == 0:
            self.x -= self.constants.SCALE_FACTOR
        elif nn_action == 1:
            self.x += self.constants.SCALE_FACTOR
        elif nn_action == 2:
            self.y -= self.constants.SCALE_FACTOR
        elif nn_action == 3:
            self.y += self.constants.SCALE_FACTOR

        self.set_sensing_rects()

        return self.x, self.y

    def sense_box(self, simulation):
        output = []

        for i in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
            for j in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
                coord = (self.x + self.constants.SCALE_FACTOR * i, self.y + self.constants.SCALE_FACTOR * j)
                if coord == (self.x, self.y):
                    continue

                    #Output for food-----------
                if coord in simulation.food:
                    output.append(1)
                else:
                    output.append(0)
                #Output for edge-----------
                if coord[0] < 0 or coord[0] > self.constants.WORLD_WIDTH or coord[1] < 0 or coord[1] > self.constants.WORLD_HEIGHT:
                    output.append(1)
                else:
                    output.append(0)

                #Output for other robots always 0 in single agent---------
                if coord in simulation.water:
                    output.append(1)
                else:
                    output.append(0)

        return output

    def sense_boxDiff(self, simulation):
        output = []

        for i in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
            for j in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
                coord = (self.x + self.constants.SCALE_FACTOR * i, self.y + self.constants.SCALE_FACTOR * j)
                if coord == (self.x, self.y):
                    continue

                #Output for food-----------
                if coord in simulation.food:
                    output.append(ContentOfSquare.Food.value)
                elif coord[0] < 0 or coord[0] > self.constants.WORLD_WIDTH or coord[1] < 0 or coord[1] > self.constants.WORLD_HEIGHT:
                    output.append(ContentOfSquare.OutsideArena.value)
                elif coord in simulation.water:
                    output.append(ContentOfSquare.Water.value)
                else:
                    output.append(ContentOfSquare.Empty.value)

        return output



    # def sense_pyramid(self, simulation):
    #     output = []
    #
    #     coords = []
    #     #height of pyramid
    #     n = SENSING_DISTANCE
    #     lr = 0
    #
    #     for i in range(n, -1, -1):
    #         y = self.y + i * SCALE_FACTOR
    #         for j in range(lr+1):
    #             x1 = self.x + SCALE_FACTOR*j
    #             x2 = self.x - SCALE_FACTOR*j
    #             coords.append((x1, y))
    #             coords.append((x2, y))
    #         lr += 1
    #
    #     lr = 0
    #     for i in range(n, 0, -1):
    #         y = self.y - i * SCALE_FACTOR
    #         for j in range(lr+1):
    #             x1 = self.x + SCALE_FACTOR*j
    #             x2 = self.x - SCALE_FACTOR*j
    #             coords.append((x1, y))
    #             coords.append((x2, y))
    #         lr += 1
    #
    #     coords.remove((self.x, self.y))
    #
    #     self.sensing_rects_before_move = coords
    #
    #     for coord in coords:
    #         if coord in simulation.food:
    #             output.append(1)
    #         elif coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
    #             output.append(0)
    #         else:
    #             output.append(0.5)
    #
    #     return output

    def set_sensing_rects(self):
        self.sensing_rects = []
        for i in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
            for j in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
                coord = (self.x + self.constants.SCALE_FACTOR * i, self.y + self.constants.SCALE_FACTOR * j)
                if coord == (self.x, self.y):
                    continue
                else:
                    self.sensing_rects.append(coord)

