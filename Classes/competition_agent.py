import pygame
import neat
import queue
from Classes.constants import Constants, SensingMode, ContentOfSquare


class CompetitionAgent:
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
        #rect.center = (self.x, self.y)
        return rect

    def move(self, simulation):
        if self.previous_positions.full():
            self.previous_positions.get()
        self.previous_positions.put((self.x, self.y))

        if self.sensing_mode == SensingMode.BoxDiff:
            sensed = self.sense_boxDiff(simulation)
        elif self.sensing_mode == SensingMode.Box:
            sensed = self.sense_box(simulation)

        sensed.append(self.x / self.constants.WORLD_WIDTH)
        sensed.append(self.y / self.constants.WORLD_HEIGHT)
        sensed.append(self.energy / self.constants.ALLOWED_MOVES_WITHOUT_PROGRESS)

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

        return self.x, self.y

    def sense_box(self, simulation):
        output = []
        self.sensing_rects_before_move = []
        other_agent_coords = [(a.x, a.y) for a in simulation.population]

        for i in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
            for j in range(-self.constants.SENSING_DISTANCE, self.constants.SENSING_DISTANCE + 1):
                coord = (self.x + self.constants.SCALE_FACTOR * i, self.y + self.constants.SCALE_FACTOR * j)
                if coord == (self.x, self.y):
                    continue
                else:
                    self.sensing_rects_before_move.append(coord)

                    # Output for food-----------
                    if coord in simulation.food:
                        output.append(1)
                    else:
                        output.append(0)
                    # Output for edge-----------
                    if coord[0] < 0 or coord[0] > self.constants.WORLD_WIDTH or coord[1] < 0 or coord[1] > self.constants.WORLD_HEIGHT:
                        output.append(1)
                    else:
                        output.append(0)

                    # Output for other robots---------
                    if coord in other_agent_coords:
                        output.append(1)
                    else:
                        output.append(0)
        return output


    def sense_boxDiff(self, simulation):
        output = []
        other_agent_coords = [(a.x, a.y) for a in simulation.population]

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
                elif coord in other_agent_coords:
                    output.append(ContentOfSquare.OtherRobot.value)
                else:
                    output.append(ContentOfSquare.Empty.value)

        return output
