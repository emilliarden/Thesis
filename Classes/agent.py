import copy
import pygame
from numpy import random, sin, cos
from Classes.neural_network import NeuralNetwork
from Classes.constants import WORLD_HEIGHT, WORLD_WIDTH, SCALE_FACTOR

possible_directions = [(SCALE_FACTOR, 0), (-SCALE_FACTOR, 0), (0, SCALE_FACTOR), (0, -SCALE_FACTOR)]
start_position = (WORLD_WIDTH/2, WORLD_HEIGHT/2)
robot_timestep = 0.1        # 1/robot_timestep equals update frequency of robot
simulation_timestep = 0.01

class Agent:
    def __init__(self):
        self.x = start_position[0]
        self.y = start_position[1]
        self.q = 0
        self.size = SCALE_FACTOR
        self.age = 0
        self.energy = 200
        self.color = (random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.nn = NeuralNetwork()
        self.out_of_bounds = False
        self.radius_of_wheels = 20
        self.distance_between_wheels = 100
        self.left_wheel_velocity = 0
        self.right_wheel_velocity = 0

    def get_direction_line(self):
        if self.q == 0:
            return (self.rect.midtop, (self.rect.midtop[0], self.rect.midtop[1] -5))
        elif self.q == 90:
            return (self.rect.midright, (self.rect.midright[0]+5, self.rect.midright[1]) )
        elif self.q == 180:
            return (self.rect.midbottom, (self.rect.midbottom[0], self.rect.midbottom[1] + 5))
        else:
            return (self.rect.midleft, (self.rect.midleft[0]-5, self.rect.midleft[1]))

    def sense(self, food, water, population, timestep):
        amount_of_food_in_direction_q = 0
        amount_of_robots_in_direction_q = 0
        amount_of_water_in_direction_q = 0
        amount_of_nothing_in_direction_q = 0

        agent_rects = [pygame.Rect(r.x, r.y, r.size, r.size) for r in population]

        loop_x_end = self.x
        if self.q == 90:
            loop_x_end = WORLD_WIDTH
        if self.q == 270:
            loop_x_end = 0

        loop_y_end = self.y 
        if self.q == 0:
            loop_y_end = 0  
        if self.q == 180:
            loop_y_end = WORLD_HEIGHT

        y_loop_start = int(min([self.y, loop_y_end]))
        y_loop_end = int(max([self.y, loop_y_end]))
        x_loop_start = int(min([self.x, loop_x_end]))
        x_loop_end = int(max([self.x, loop_x_end]))

        first = True
        set_water_to_max = False

        for x in range(x_loop_start, x_loop_end+1, 10):
            for y in range(y_loop_start, y_loop_end+1, 10):
                rect = pygame.Rect(x, y, self.size, self.size)
                if rect.collidelist(food) > -1:
                    amount_of_food_in_direction_q += 1
                elif rect.collidelist(water) > -1:
                    if first:
                        set_water_to_max = True
                    amount_of_water_in_direction_q += 1
                elif rect.collidelist(agent_rects) > -1:
                    amount_of_robots_in_direction_q += 1
                else:
                    amount_of_nothing_in_direction_q += 1
                first = False

        total_squares_in_direction_q = amount_of_food_in_direction_q + amount_of_robots_in_direction_q + amount_of_water_in_direction_q + amount_of_nothing_in_direction_q
        amount_of_water_in_direction_q = total_squares_in_direction_q if set_water_to_max else amount_of_water_in_direction_q
        return [self.x/WORLD_WIDTH, self.y/WORLD_HEIGHT, self.age, amount_of_food_in_direction_q/total_squares_in_direction_q, amount_of_robots_in_direction_q/total_squares_in_direction_q, amount_of_water_in_direction_q/total_squares_in_direction_q]

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
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def set_motor_speeds(self, nn_output):
        self.left_wheel_velocity = nn_output[0]
        self.right_wheel_velocity = nn_output[1]


    def move_robot(self, action):
        if action == 2:
            if self.q == 270:
                self.q = 0
            else:
                self.q += 90 
        if action == 1:
            if self.q == 0:
                self.q = 270
            else:
                self.q -= 90
        if action == 0:
            if self.q == 0:
                self.y = self.y - 10
            if self.q == 90:
                self.x = self.x + 10
            if self.q == 180:
                self.y = self.y + 10
            if self.q == 270:
                self.x = self.x - 10
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def get_robot_rect_from_move(self, action):
        x, y, q = self.x, self.y, self.q
        
        if action == 2:
            if self.q == 270:
                q = 0
            else:
                q = self.q + 90
        if action == 1:
            if self.q == 0:
                q = 270
            else:
                q = self.q - 90
        if action == 0:
            if self.q == 0:
                y = self.y - 10
            if self.q == 90:
                x = self.x + 10
            if self.q == 180:
                y = self.y + 10
            if self.q == 270:
                x = self.x - 10

        return pygame.Rect(x, y, self.size, self.size)
       
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
        new_agent.energy = 100
        return new_agent
