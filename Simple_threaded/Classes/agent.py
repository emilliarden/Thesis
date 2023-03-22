import pygame
import neat
import numpy as np
import queue
from Simple_threaded.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR, SENSING_DISTANCE, START_POSITION, SensingMode


class Agent:
    def __init__(self, genome, config, food, sensing_mode):
        self.x = START_POSITION[0]
        self.y = START_POSITION[1]
        self.size = SCALE_FACTOR
        self.color = (200, 8, 8)
        self.sensing_distance = SENSING_DISTANCE
        self.previous_positions = queue.Queue(10)
        self.genome = genome
        self.genome.fitness = 0
        self.nn = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        self.out_of_bounds = False
        self.best_move = False
        self.timesteps_without_progress = 0
        self.timesteps_alive = 0
        self.food = food
        self.sensing_mode = sensing_mode

    def get_center_coord(self):
        return self.x, self.y

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect

    def move(self):
        if self.previous_positions.full():
            self.previous_positions.get()
        self.previous_positions.put((self.x, self.y))

        if self.sensing_mode == SensingMode.Pyramid:
            sensed = self.sense_pyramid()
        elif self.sensing_mode == SensingMode.Box:
            sensed = self.sense_box()
        elif self.sensing_mode == SensingMode.Cross:
            sensed = self.sense_cross()

        sensed.append(self.x / WORLD_WIDTH)
        sensed.append(self.y / WORLD_HEIGHT)

        return self.x, self.y


    def sense_box(self):
        output = []

        coords = []
        for i in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
            for j in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
                coords.append((self.x + SCALE_FACTOR * i, self.y + SCALE_FACTOR * j))

        coords.remove((self.x, self.y))


        self.sensing_rects_before_move = coords

        for coord in coords:
            if coord in self.food:
                output.append(1)
            elif coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(0)
            else:
                output.append(0.5)

        if 0 not in output:
            x = 15
            pass

        return output


