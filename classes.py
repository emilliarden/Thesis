import pygame
from numpy import exp, array, random, dot
from NN import NeuralNetwork
 
 
SCALE_FACTOR = 10
possible_directions = [(SCALE_FACTOR,0), (-SCALE_FACTOR,0), (0,SCALE_FACTOR), (0,-SCALE_FACTOR)]
world_height = 800
world_width = 800
timesteps = 1000
start_position = (world_width/2, world_height/2)

class Robot:
    def __init__(self, moves=[]):
        self.x = start_position[0]
        self.y = start_position[1]
        self.q = 0
        self.size = SCALE_FACTOR
        self.foodGathered = 0
        self.color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
        self.nn = NeuralNetwork()
        self.out_of_bounds = False

    def get_direction_line(self):
        current_rect = pygame.Rect(self.x, self.y, self.size, self.size)


        if self.q == 0:
            return (current_rect.midtop, (current_rect.midtop[0], current_rect.midtop[1] -5))
        elif self.q == 90:
            return (current_rect.midright, (current_rect.midright[0]+5, current_rect.midright[1]) ) 
        elif self.q == 180:
            return (current_rect.midbottom, (current_rect.midbottom[0], current_rect.midbottom[1] + 5))
        else:
            return (current_rect.midleft, (current_rect.midleft[0]-5, current_rect.midleft[1]) )  

    def sense(self, food_rects, water_rects, robots, timestep):        
        amount_of_food_in_direction_q = 0
        amount_of_robots_in_direction_q = 0
        amount_of_water_in_direction_q = 0
        amount_of_nothing_in_direction_q = 0

        robot_rects = [pygame.Rect(r.x,r.y,r.size, r.size) for r in robots]

        loop_x_end = self.x
        if self.q == 90:
            loop_x_end = world_width
        if self.q == 270:
            loop_x_end = 0

        loop_y_end = self.y 
        if self.q == 0:
            loop_y_end = 0  
        if self.q == 180:
            loop_y_end = world_height

        y_loop_start = int(min([self.y, loop_y_end]))
        y_loop_end = int(max([self.y, loop_y_end]))
        x_loop_start = int(min([self.x, loop_x_end]))
        x_loop_end = int(max([self.x, loop_x_end]))

        squares_to_water = 1000

        for x in range(x_loop_start, x_loop_end+1, 10):
            for y in range(y_loop_start, y_loop_end+1, 10):
                rect = pygame.Rect(x, y, self.size, self.size)
                if rect.collidelist(food_rects) > -1:
                    amount_of_food_in_direction_q += 1
                elif rect.collidelist(water_rects) > -1:
                    amount_of_water_in_direction_q += 1
                elif rect.collidelist(robot_rects) > -1:
                    amount_of_robots_in_direction_q += 1
                else:
                    amount_of_nothing_in_direction_q += 1

        total_squares_in_direction_q = amount_of_food_in_direction_q + amount_of_robots_in_direction_q + amount_of_water_in_direction_q + amount_of_nothing_in_direction_q
        return [amount_of_food_in_direction_q/total_squares_in_direction_q, amount_of_robots_in_direction_q/total_squares_in_direction_q, amount_of_water_in_direction_q/total_squares_in_direction_q, timestep/800]

        

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

    def get_robot_rect_from_move(self, action):
        x,y,q = self.x, self.y, self.q
        
        if action == 2:
            if self.q == 270:
                q = 0
            else:
                q= self.q + 90 
        if action == 1:
            if self.q == 0:
                q = 270
            else:
                q = self.q - 90
        if action == 0:
            if self.q == 0:
                y = self.y - 10
            if self.q == 90:
                x= self.x + 10
            if self.q == 180:
                y = self.y + 10
            if self.q == 270:
                x = self.x - 10

        return pygame.Rect(x,y, self.size, self.size)
       
    def reset_robot(self):
        self.x = world_width/2
        self.y = world_height/2
        self.q = 0

    def mutate(self):
        nn_layers = self.nn.input_layer+self.nn.hidden_layer+self.nn.output_layer
        random_index = random.randint(0, len(nn_layers)-1)
        nn_layers[random_index].bias = random.uniform(-1,1)
        nn_layers[random_index].weight = random.uniform(-4,4)

        self.color =  (random.randint(1,255), random.randint(1,255), random.randint(1,255))


    def printStatus(self):
        print("-----------")
        print("x: " + str(self.x) + " y: " + str(self.y))
        print("rect: " + str(self.rect))
        print("FoodGathered: " + str(self.foodGathered))
        print("-----------")


class Food:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = SCALE_FACTOR
        self.rect = pygame.Rect(self.x,self.y, self.size, self.size)

    def init_x_and_y(self):
        self.x = random.randint(0,world_width)
        self.y = random.randint(0,world_height)


class Food2:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size = 10
        self.rect = pygame.Rect(self.x,self.y, self.size, self.size)
        self.moves = []



class Water:
    def __init__(self):
        randomcenter_x = random.randint(0, world_width)
        randomcenter_y = random.randint(0, world_height)
        random_size = random.randint(30, 100)
        self.rect = pygame.Rect(randomcenter_x, randomcenter_y, random_size, random_size)
        # self.top_left = (random.randint(0,800), random.randint(0,800))
        # self.top_right = (random.randint(self.top_left[0], self.top_left[0]+100), self.top_left[1])
        # self.bottom_left = (self.top_left[0], random.randint(self.top_left[1], self.top_left[1]+100))
        # self.bottom_right = (self.top_right[0], self.bottom_left[1])
        # self.points = [self.top_left, self.bottom_left, self.bottom_right, self.top_right]