import pygame
import numpy as np
import queue
from Simple.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR, SENSING_DISTANCE


class Agent:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.size = SCALE_FACTOR
        self.color = (np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255))
        self.sensing_distance = SENSING_DISTANCE
        self.sensing_rects_before_move = []
        self.sensing_rects_after_move = []
        self.previous3_positions = queue.Queue(10)
        self.nn = None
        self.genome = None
        self.out_of_bounds = False
        self.previous_locations = [(self.x, self.y)]
        self.sensed_food_nearest_square = False
        self.sensed_food_second_square = False
        self.amount_of_sensed_food = 0
        self.best_move = False

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
        if self.previous3_positions.full():
            self.previous3_positions.get()

        self.previous3_positions.put((self.x, self.y))


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

        # self.best_move = nn_action == best_move

        coords = []
        for i in range(1, SENSING_DISTANCE + 1):
            coords.append((self.x, self.y - SCALE_FACTOR * i))
            coords.append((self.x + SCALE_FACTOR * i, self.y))
            coords.append((self.x, self.y + SCALE_FACTOR * i))
            coords.append((self.x - SCALE_FACTOR * i, self.y))

        self.sensing_rects_after_move = coords

        return self.x, self.y

    def sense2(self, simulation):
        output = []
        robot_coords = []

        # list(filter(lambda a: a.out_of_bounds is False, simulation.population))
        # robot_coords = set([a.get_center_coord() for a in robots])

        coords = []
        for i in range(1, SENSING_DISTANCE + 1):
            coords.append((self.x, self.y - SCALE_FACTOR * i))
            coords.append((self.x + SCALE_FACTOR * i, self.y))
            coords.append((self.x, self.y + SCALE_FACTOR * i))
            coords.append((self.x - SCALE_FACTOR * i, self.y))

        self.sensing_rects_before_move = coords

        for i, coord in enumerate(coords):
            if coord in simulation.food:
                output.append(1)
            elif coord in robot_coords or coord[0] < 0 or coord[0] > WORLD_WIDTH or coord[1] < 0 or coord[1] > WORLD_HEIGHT:
                output.append(0)
            else:
                output.append(0.5)

        # output.append(self.x/WORLD_WIDTH)
        # output.append(self.y/WORLD_HEIGHT)

        if 1 in output[:4]:
            self.sensed_food_nearest_square = True
        else:
            self.sensed_food_nearest_square = False

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

        if 1 in output[:4]:
            self.sensed_food_nearest_square = True
        else:
            self.sensed_food_nearest_square = False

        return output

    def simulation_step(self, simulation) -> bool:
        pass

    def simulation_step_rect(self):
        pass
