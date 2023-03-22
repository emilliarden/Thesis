import copy
import math

import pygame
import numpy as np
from scipy.spatial.distance import cdist
from Advanced.Classes.neural_network import NeuralNetwork
from Advanced.Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR
from Advanced.Classes.geometry_functions import intersect, angle_between, point_inside_polygon

start_position = (WORLD_WIDTH/2, WORLD_HEIGHT/2)
robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01
INITIAL_ENERGY = 0

class Agent:
    def __init__(self):
        self.x = start_position[0]
        self.y = start_position[1]
        self.q = 0
        self.size = SCALE_FACTOR
        self.age = 0
        self.energy = INITIAL_ENERGY
        self.color = (np.random.randint(1, 255), np.random.randint(1, 255), np.random.randint(1, 255))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.nn = NeuralNetwork()
        self.out_of_bounds = False
        self.radius_of_wheels = 60
        self.distance_between_wheels = 80
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0
        self.sensing_distance = 250
        self.sensing_rect = None

    def get_center_coord(self):
        return (self.x, self.y)

    def get_sensing_points(self):
        direction_of_agent = self.q
        angle = 20*np.pi/180
        angle_12 = 90*np.pi/180
        angle1 = direction_of_agent - (angle)
        angle2 = direction_of_agent + (angle)
        angle3 = direction_of_agent + angle_12
        angle4 = direction_of_agent - angle_12

        point1_x = self.x + self.sensing_distance * np.cos(angle1)
        point1_y = self.y + self.sensing_distance * np.sin(angle1)

        point2_x = self.x + self.sensing_distance * np.cos(angle2)
        point2_y = self.y + self.sensing_distance * np.sin(angle2)

        point3_x = self.x + 5 * np.cos(angle3)
        point3_y = self.y + 5 * np.sin(angle3)

        point4_x = self.x + 5 * np.cos(angle4)
        point4_y = self.y + 5 * np.sin(angle4)

        return [(point1_x, point1_y), (point2_x, point2_y), (point3_x, point3_y), (point4_x, point4_y)]

    def sense(self, food, water, population, quad_tree):

        sensing_rect = self.get_sensing_points()

        #FOOD-------------------------------
        minX = min([x[0] for x in sensing_rect])
        minY = min([x[1] for x in sensing_rect])
        maxX = max([x[0] for x in sensing_rect])
        maxY = max([x[1] for x in sensing_rect])

        self.sensing_rect = pygame.Rect(minX, minY, maxX-minX, maxY-minY)

        sensed_food = quad_tree.range_search([(minX, minY), (maxX, maxY)])
        sensed_food = list(filter(lambda p: point_inside_polygon(p[0], p[1], sensing_rect), sensed_food))
        amount_of_food_in_sensing_area = len(sensed_food)
        closest_food_and_distance = self.closest_food_and_distance((self.x, self.y), sensed_food) if amount_of_food_in_sensing_area > 0 else None
        closest_food_distance = 0
        #TODO: Think about what the angle should be when no food.py is detected
        angle_to_food = 0

        if closest_food_and_distance != None:
            closest_food = closest_food_and_distance[0]
            closest_food_distance = closest_food_and_distance[1]
            #Angle to food.py:
            direction_vector = [math.cos(self.q), math.sin(self.q)]
            food_vector = [max(self.x, closest_food[0])-min(self.x, closest_food[0]), max(self.y, closest_food[1])-min(self.y, closest_food[1])]
            angle_to_food = angle_between(direction_vector, food_vector)
        #--------------------------------
        #EDGEDETECTION-------------------
        detect_edge = 0
        distance_to_edge = 0
        if (sensing_rect[0][0] < 0 or sensing_rect[1][0] < 0
                or sensing_rect[0][0] > WORLD_WIDTH or sensing_rect[1][0] > WORLD_WIDTH
                or sensing_rect[0][1] < 0 or sensing_rect[1][1] < 0
                or sensing_rect[0][1] > WORLD_HEIGHT or sensing_rect[1][1] > WORLD_HEIGHT):
            distance_to_edge = self.get_distance_to_edge(sensing_rect)
            if distance_to_edge < 250:
                detect_edge = 1

        #WATER----------------------------
        # amount_of_water_in_sensing_triangle = 0
        # closest_water = 100
        # for w in water:
        #     if self.pointInTriangle(w.center, (self.x, self.y), sensing_rect[0], sensing_rect[1]):
        #         amount_of_water_in_sensing_triangle += 1
        # #--------------------------------
        # #AGENTS---------------------------
        amount_of_agents_in_sensing_area = 0
        distance_to_closest_agent = self.sensing_distance
        # TODO: Think about what the angle should be when no agent.py is detected
        angle_to_closest_agent = 0
        for a in population:
            if point_inside_polygon(a.x, a.y, sensing_rect):
                amount_of_agents_in_sensing_area += 1
                distance_to_agent = math.dist(self.get_center_coord(), a.get_center_coord())
                if distance_to_agent < distance_to_closest_agent:
                    distance_to_closest_agent = distance_to_agent
                    direction_vector = [math.cos(self.q), math.sin(self.q)]
                    agent_vector = [max(self.x, a.x) - min(self.x, a.x),
                                    max(self.y, a.y) - min(self.y, a.y)]
                    angle_to_closest_agent = angle_between(direction_vector, agent_vector)

        # if (amount_of_agents_in_sensing_area > 0):
        #     print("COLOR: " + str(self.color))
        #     print("Amount of agents in sensing area: " + str(amount_of_agents_in_sensing_area))

        #-------------------------------
        return [amount_of_food_in_sensing_area/len(food),
                (self.sensing_distance - closest_food_distance)/self.sensing_distance,
                angle_to_food, detect_edge, distance_to_edge, self.age/(sum(x.age for x in population)+1),
                amount_of_agents_in_sensing_area/len(population), (self.sensing_distance - distance_to_closest_agent)/self.sensing_distance,
                angle_to_closest_agent]

    def get_distance_to_edge(self, sensing_rect):
        sensing_line = [sensing_rect[1], sensing_rect[0]]
        border_lines = [((0, 0), (WORLD_WIDTH, 0)),
                       ((0, 0), (0, WORLD_HEIGHT)),
                       ((0, WORLD_HEIGHT), (WORLD_WIDTH, WORLD_HEIGHT)),
                       ((WORLD_WIDTH, WORLD_HEIGHT), (WORLD_WIDTH, 0))]

        direction_of_agent = self.q
        point1_x = self.x + WORLD_WIDTH * np.cos(direction_of_agent)
        point1_y = self.y + WORLD_HEIGHT * np.sin(direction_of_agent)
        sensing_line = [self.get_center_coord(), (point1_x, point1_y)]

        distance_to_return = self.sensing_distance
        for line in border_lines:
            intersection_point = intersect(sensing_line[0], sensing_line[1], line[0], line[1])
            if intersection_point != None:
                #intersection_point = line_intersection(sensing_line, line)
                distance = math.dist(self.get_center_coord(), intersection_point)
                if distance < distance_to_return:
                    distance_to_return = distance
                # print("Current coord: " + str(self.get_center_coord()))
                # print("Current direction: " + str(self.q))
                # print("Intersection point: " + str(intersection_point))
                # print("Distance between: " + str(distance))

        return distance_to_return




    def closest_food_and_distance(self, pt, pts):
        closest_food = pts[cdist([pt], pts).argmin()]
        return (closest_food, math.dist(closest_food, (self.x, self.y)))

    def sign(self, p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])


    def simulation_step(self):
        for step in range(int(robot_timestep / simulation_timestep)):  # step model time/timestep times
            v_x = np.cos(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            v_y = np.sin(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            omega = (self.radius_of_wheels * self.right_wheel_velocity - self.radius_of_wheels * self.left_wheel_velocity) / (2 * self.distance_between_wheels)

            self.x += v_x * simulation_timestep
            self.y += v_y * simulation_timestep
            self.q += omega * simulation_timestep

    def simulation_step_rect(self):
        x = self.x
        y = self.y
        q = self.q

        for step in range(int(robot_timestep / simulation_timestep)):  # step model time/timestep times
            v_x = np.cos(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
            v_y = np.sin(self.q) * (self.radius_of_wheels * self.left_wheel_velocity / 2 + self.radius_of_wheels * self.right_wheel_velocity / 2)
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
        random_index = np.random.randint(0, len(nn_layers)-1)
        nn_layers[random_index].bias = np.random.uniform(-1,1)
        nn_layers[random_index].weight = np.random.uniform(-4,4)

        self.color = (np.random.randint(1,255), np.random.randint(1,255), np.random.randint(1,255))


    def create_offspring(self):
        new_agent = copy.deepcopy(self)
        new_agent.mutate()
        new_agent.x = np.random.randint(0, WORLD_WIDTH)
        new_agent.y = np.random.randint(0, WORLD_HEIGHT)
        new_agent.rect = pygame.Rect(new_agent.x, new_agent.y, SCALE_FACTOR, SCALE_FACTOR)
        new_agent.energy = INITIAL_ENERGY
        new_agent.age = 0
        return new_agent
