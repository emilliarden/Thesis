import pygame
import neat
import random
import numpy as np
import queue
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR, SENSING_DISTANCE, START_POSITION, SensingMode


class Agent:
    def __init__(self, genome, config, sensing_mode):
        self.x = START_POSITION[0]
        self.y = START_POSITION[1]
        #self.x = round(random.randint(0, WORLD_WIDTH) / SCALE_FACTOR) * SCALE_FACTOR
        #self.y = round(random.randint(0, WORLD_HEIGHT) / SCALE_FACTOR) * SCALE_FACTOR
        self.size = SCALE_FACTOR
        self.color = (200, 8, 8)
        self.sensing_distance = SENSING_DISTANCE
        self.sensing_rects_before_move = []
        self.sensing_rects_after_move = []
        self.previous_positions = queue.Queue(10)
        self.genome = genome
        self.nn = neat.nn.RecurrentNetwork.create(genome, config)
        self.out_of_bounds = False
        self.amount_of_sensed_food = 0
        self.best_move = False
        self.timesteps_without_progress = 0
        self.timesteps_alive = 0
        self.sensing_mode = sensing_mode
        self.visited_squares = set()
        self.previous_output = [0,0,0,0]

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


        sensed.append(self.x/WORLD_WIDTH)
        sensed.append(self.y/WORLD_HEIGHT)

        nn_output = self.nn.activate(sensed + self.previous_output)
        self.previous_output = nn_output
        nn_action = nn_output.index(max(nn_output))

        if nn_action == 0:
            self.x -= SCALE_FACTOR
        elif nn_action == 1:
            self.x += SCALE_FACTOR
        elif nn_action == 2:
            self.y -= SCALE_FACTOR
        elif nn_action == 3:
            self.y += SCALE_FACTOR

        # coords = []
        # for i in range(1, SENSING_DISTANCE + 1):
        #     coords.append((self.x, self.y - SCALE_FACTOR * i))
        #     coords.append((self.x + SCALE_FACTOR * i, self.y))
        #     coords.append((self.x, self.y + SCALE_FACTOR * i))
        #     coords.append((self.x - SCALE_FACTOR * i, self.y))
        #
        # self.sensing_rects_after_move = coords
        return self.x, self.y

    def sense_box(self, simulation):
        output = []

        coords = []
        for i in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
            for j in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
                coords.append((self.x + SCALE_FACTOR * i, self.y + SCALE_FACTOR * j))

        coords.remove((self.x, self.y))


        self.sensing_rects_before_move = coords

        for coord in coords:
            if coord in simulation.food:
                output.append(1)
            elif coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(0)
            else:
                output.append(0.5)

        if 0 not in output:
            x = 15
            pass

        return output

    def sense_cross(self, simulation):
        output = []

        coords = []
        for i in range(1, SENSING_DISTANCE + 1):
            coords.append((self.x, self.y - SCALE_FACTOR * i))
            coords.append((self.x + SCALE_FACTOR * i, self.y))
            coords.append((self.x, self.y + SCALE_FACTOR * i))
            coords.append((self.x - SCALE_FACTOR * i, self.y))

        self.sensing_rects_before_move = coords

        for coord in coords:
            if coord in simulation.food:
                output.append(1)
            elif coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(0)
            else:
                output.append(0.5)

        return output

    def sense_pyramid(self, simulation):
        output = []

        coords = []
        #height of pyramid
        n = SENSING_DISTANCE
        lr = 0

        for i in range(n, -1, -1):
            y = self.y + i * SCALE_FACTOR
            for j in range(lr+1):
                x1 = self.x + SCALE_FACTOR*j
                x2 = self.x - SCALE_FACTOR*j
                coords.append((x1, y))
                coords.append((x2, y))
            lr += 1

        lr = 0
        for i in range(n, 0, -1):
            y = self.y - i * SCALE_FACTOR
            for j in range(lr+1):
                x1 = self.x + SCALE_FACTOR*j
                x2 = self.x - SCALE_FACTOR*j
                coords.append((x1, y))
                coords.append((x2, y))
            lr += 1

        coords.remove((self.x, self.y))

        self.sensing_rects_before_move = coords

        for coord in coords:
            if coord in simulation.food:
                output.append(1)
            elif coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(0)
            else:
                output.append(0.5)

        return output

    def get_4_nearest_squares(self):
        return [(self.x, self.y - SCALE_FACTOR),
                (self.x + SCALE_FACTOR, self.y),
                (self.x, self.y + SCALE_FACTOR),
                (self.x - SCALE_FACTOR, self.y)]
