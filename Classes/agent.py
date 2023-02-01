import copy
import pygame
from numpy import random, sin, cos, pi, array, linalg
from Classes.neural_network import NeuralNetwork
from Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR

possible_directions = [(SCALE_FACTOR, 0), (-SCALE_FACTOR, 0), (0, SCALE_FACTOR), (0, -SCALE_FACTOR)]
start_position = (WORLD_WIDTH/2, WORLD_HEIGHT/2)
robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01
INITIAL_ENERGY = 500

class Agent:
    def __init__(self):
        self.x = start_position[0]
        self.y = start_position[1]
        self.q = 0
        self.size = SCALE_FACTOR
        self.age = 0
        self.energy = INITIAL_ENERGY
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.nn = NeuralNetwork()
        self.out_of_bounds = False
        self.radius_of_wheels = 60
        self.distance_between_wheels = 80
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0
        self.sensing_distance = 250
        self.sensing_rect = None

    def get_sensing_points(self):
        direction_of_agent = self.q
        angle = 20*pi/180
        angle_12 = 90*pi/180
        angle1 = direction_of_agent - (angle)
        angle2 = direction_of_agent + (angle)
        angle3 = direction_of_agent + angle_12
        angle4 = direction_of_agent - angle_12
        point1_x = self.x + self.sensing_distance * cos(angle1)
        point1_y = self.y + self.sensing_distance * sin(angle1)

        point2_x = self.x + self.sensing_distance * cos(angle2)
        point2_y = self.y + self.sensing_distance * sin(angle2)

        point3_x = self.x + 5 * cos(angle3)
        point3_y = self.y + 5 * sin(angle3)

        point4_x = self.x + 5 * cos(angle4)
        point4_y = self.y + 5 * sin(angle4)



        return [(point1_x, point1_y), (point2_x, point2_y), (point3_x, point3_y), (point4_x, point4_y)]

    def sense(self, food, water, population, quad_tree):

        sensing_rect = self.get_sensing_points()
        closest_food = 100

        minX = min([x[0] for x in sensing_rect])
        minY = min([x[1] for x in sensing_rect])
        maxX = max([x[0] for x in sensing_rect])
        maxY = max([x[1] for x in sensing_rect])

        #TEST
        sensing_r_test = pygame.Rect(minX, minY, maxX-minX, maxY-minY)
        #sensing_r_test.bottomleft = (minX, minY)
        #sensing_r_test.topright = (maxX, maxY)
        self.sensing_rect = sensing_r_test
        #####

        sensed_food = quad_tree.range_search([(minX, maxY), (maxX, minY)])
        amount_of_food_in_sensing_area = len(sensed_food)


        amount_of_water_in_sensing_triangle = 0
        closest_water = 100
        # for w in water:
        #     if self.pisinTri(w.center):
        #         amount_of_water_in_sensing_triangle += 1

        amount_of_agents_in_sensing_triangle = 0
        closest_agent = 100
        # for a in population:
        #     if self.pisinTri(a.get_rect().center):
        #         amount_of_agents_in_sensing_triangle += 1

        return [amount_of_food_in_sensing_area, closest_food, amount_of_water_in_sensing_triangle, closest_water,
                amount_of_agents_in_sensing_triangle, closest_agent, self.age]


    def simulation_step(self):
        for step in range(int(robot_timestep / simulation_timestep)):  # step model time/timestep times
            v_x = cos(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            v_y = sin(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            omega = (self.radius_of_wheels * self.right_wheel_velocity - self.radius_of_wheels * self.left_wheel_velocity) / (2 * self.distance_between_wheels)

            self.x += v_x * simulation_timestep
            self.y += v_y * simulation_timestep
            self.q += omega * simulation_timestep

    def simulation_step_rect(self):
        x = self.x
        y = self.y
        q = self.q

        for step in range(int(robot_timestep / simulation_timestep)):  # step model time/timestep times
            v_x = cos(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            v_y = sin(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            omega = (self.radius_of_wheels * self.right_wheel_velocity - self.radius_of_wheels * self.left_wheel_velocity) / (2 * self.distance_between_wheels)

            x += v_x * simulation_timestep
            y += v_y * simulation_timestep
            q += omega * simulation_timestep

        return pygame.Rect(x, y, self.size, self.size)

    def get_rect(self):
        rect = pygame.Rect(self.x, self.y, self.size, self.size)
        rect.center = (self.x, self.y)
        return rect

    def set_motor_speeds(self, nn_output):
        self.left_wheel_velocity = nn_output[0]
        self.right_wheel_velocity = nn_output[1]

       
    def reset_robot(self):
        self.x = WORLD_WIDTH/2
        self.y = WORLD_HEIGHT/2
        self.q = 0

    def mutate(self):
        nn_layers = self.nn.input_layer+self.nn.hidden_layer+self.nn.output_layer
        random_index = random.randint(0, len(nn_layers)-1)
        nn_layers[random_index].bias = random.uniform(-1,1)
        nn_layers[random_index].weight = random.uniform(-4,4)

        self.color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))


    def create_offspring(self):
        new_agent = copy.deepcopy(self)
        new_agent.mutate()
        new_agent.x = random.randint(0, WORLD_WIDTH)
        new_agent.y = random.randint(0, WORLD_HEIGHT)
        new_agent.rect = pygame.Rect(new_agent.x, new_agent.y, SCALE_FACTOR, SCALE_FACTOR)
        new_agent.energy = INITIAL_ENERGY
        new_agent.age = 0
        return new_agent
