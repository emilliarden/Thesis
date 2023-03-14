import pygame
import neat
import numpy as np
import queue
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR, SENSING_DISTANCE, START_POSITION


class Agent:
    def __init__(self, genome, config):
        self.x = START_POSITION[0]
        self.y = START_POSITION[1]
        self.size = SCALE_FACTOR
        self.color = (200, 8, 8)
        self.sensing_distance = SENSING_DISTANCE
        self.sensing_rects_before_move = []
        self.sensing_rects_after_move = []
        self.previous_positions = queue.Queue(10)
        self.genome = genome
        self.nn = neat.nn.recurrent.RecurrentNetwork.create(genome, config)
        self.out_of_bounds = False
        self.amount_of_sensed_food = 0
        self.best_move = False
        self.timesteps_without_progress = 0
        self.timesteps_alive = 0

    def get_center_coord(self):
        return self.x, self.y

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect

    def get_best_move(self, simulation):
        coords = [(self.x, self.y - SCALE_FACTOR), (self.x + SCALE_FACTOR, self.y),
                  (self.x, self.y + SCALE_FACTOR), (self.x - SCALE_FACTOR, self.y),
                  (self.x, self.y - SCALE_FACTOR * 2), (self.x + SCALE_FACTOR * 2, self.y),
                  (self.x, self.y + SCALE_FACTOR * 2), (self.x - SCALE_FACTOR * 2, self.y),
                  (self.x, self.y - SCALE_FACTOR * 3), (self.x + SCALE_FACTOR * 3, self.y),
                  (self.x, self.y + SCALE_FACTOR * 3), (self.x - SCALE_FACTOR * 3, self.y)]

        west = [coords[3], coords[7], coords[11]]
        east = [coords[1], coords[5], coords[9]]
        north = [coords[0], coords[4], coords[8]]
        south = [coords[2], coords[6], coords[10]]

        directions = [west, east, north, south]

        best_direction_count = 0
        best_direction_index = 0

        for i, l in enumerate(directions):
            count_of_food = 0
            for coord in l:
                if coord in simulation.food:
                    count_of_food += 1
            if count_of_food > best_direction_count:
                best_direction_index = i

        return best_direction_index

    def move(self, simulation):
        if self.previous_positions.full():
            self.previous_positions.get()
        self.previous_positions.put((self.x, self.y))

        sensed = self.sense3(simulation)
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

        # coords = []
        # for i in range(1, SENSING_DISTANCE + 1):
        #     coords.append((self.x, self.y - SCALE_FACTOR * i))
        #     coords.append((self.x + SCALE_FACTOR * i, self.y))
        #     coords.append((self.x, self.y + SCALE_FACTOR * i))
        #     coords.append((self.x - SCALE_FACTOR * i, self.y))
        #
        # self.sensing_rects_after_move = coords

        return self.x, self.y

    def sense2(self, simulation):
        output = []
        robot_coords = []

        # list(filter(lambda a: a.out_of_bounds is False, simulation.population))
        # robot_coords = set([a.get_center_coord() for a in robots])

        coords = set()
        for i in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
            for j in range(-SENSING_DISTANCE, SENSING_DISTANCE + 1):
                coords.add((self.x + SCALE_FACTOR * i, self.y + SCALE_FACTOR * j))

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

    def sense3(self, simulation):
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
            else:
                output.append(0)

            if coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(1)
            else:
                output.append(0)

        #output.append(self.x/WORLD_WIDTH)
        #output.append(self.y/WORLD_HEIGHT)

        return output

    def sense4(self, simulation):
        output = []

        coords = set()
        #height of pyramid
        n = SENSING_DISTANCE
        lr = 0

        for i in range(n, -1, -1):
            y = self.y + i * SCALE_FACTOR
            for j in range(lr+1):
                x1 = self.x + SCALE_FACTOR*j
                x2 = self.x - SCALE_FACTOR*j
                coords.add((x1, y))
                coords.add((x2, y))
            lr += 1

        lr = 0
        for i in range(n, 0, -1):
            y = self.y - i * SCALE_FACTOR
            for j in range(lr+1):
                x1 = self.x + SCALE_FACTOR*j
                x2 = self.x - SCALE_FACTOR*j
                coords.add((x1, y))
                coords.add((x2, y))
            lr += 1

        coords.remove((self.x, self.y))

        self.sensing_rects_before_move = coords

        for coord in coords:

            if coord in simulation.food:
                output.append(1)
            else:
                output.append(0)

            if coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(1)
            else:
                output.append(0)

        output.append(self.x / WORLD_WIDTH)
        output.append(self.y / WORLD_HEIGHT)

        return output

    def get_4_nearest_squares(self):
        return [(self.x, self.y - SCALE_FACTOR),
                (self.x + SCALE_FACTOR, self.y),
                (self.x, self.y + SCALE_FACTOR),
                (self.x - SCALE_FACTOR, self.y)]
