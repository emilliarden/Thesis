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
        self.size = SCALE_FACTOR
        self.foodGathered = 0
        self.color = (random.randint(1,255), random.randint(1,255), random.randint(1,255))
        self.nn = NeuralNetwork()
        # self.fitness = -1000
        # self.moves = []
        # self.coordinates = []
        # self.createMoves()

    def sense(self, food, robots):
        output_arr = []
        # for x in range(int(self.x-SCALE_FACTOR), int(self.x+SCALE_FACTOR)+1, SCALE_FACTOR):
        #     for y in range(int(self.y-SCALE_FACTOR), int(self.y+SCALE_FACTOR)+1, SCALE_FACTOR):
        #         rect = pygame.rect.Rect(x,y,self.size,self.size)
        #         if (rect.collidelist(food) > 0):
        #             output_arr.append(1)
        #         elif(rect.collidelist([pygame.Rect(r.x, r.y, r.size, r.size) for r in robots])):
        #             output_arr.append(-1)
        #         else:
        #             output_arr.append(0)
        # output_arr.pop(5)

        current_rect = pygame.Rect(self.x,self.y, self.size, self.size)
        rect_list = [pygame.Rect(self.x -10, self.y, self.size, self.size), pygame.Rect(self.x +10, self.y, self.size, self.size), pygame.Rect(self.x, self.y + 10, self.size, self.size), pygame.Rect(self.x, self.y - 10, self.size, self.size)]
        robot_rect_list = [pygame.Rect(r.x, r.y, r.size, r.size) for r in robots]
        for r in rect_list:
            if r.collidelist(food) > 0:
                output_arr.append(3)
            elif r.collidelist(robot_rect_list) > 0:
                output_arr.append(1)
            elif r.x >= world_width or r.x < world_width or r.y >= world_height or r.y < 0:
                output_arr.append(-1)
            else:
                output_arr.append(2)


        return output_arr

        

    def move_robot(self, direction):
        self.x = self.x + direction[0]
        self.y = self.y + direction[1]

    def reset_robot(self):
        self.x = world_width/2
        self.y = world_height/2

    def mutate(self):
        layer_to_mutate = random.randint(1,10)

        if (layer_to_mutate <= 8):
            index = random.randint(0,len(self.nn.input_layer))
            newWeight = random.uniform(-1,1)
            newBias = random.uniform(-1,1)
            self.nn.input_layer[index].weight = newWeight
            self.nn.input_layer[index].bias = newBias
        elif (layer_to_mutate >= 9):
            index = random.randint(0, len(self.nn.output_layer))
            newWeight = random.uniform(-1,1)
            newBias = random.uniform(-1,1)
            self.nn.output_layer[index].weight = newWeight
            self.nn.output_layer[index].bias = newBias



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
        self.top_left = (random.randint(0,800), random.randint(0,800))
        self.top_right = (random.randint(self.top_left[0], self.top_left[0]+100), random.randint(self.top_left[1]-10, self.top_left[1]+10))
        self.bottom_left = (random.randint(self.top_left[0]-10, self.top_left[0]+10), random.randint(self.top_left[1], self.top_left[1]+100))
        self.bottom_right = (random.randint(self.top_right[0]-10, self.top_right[0]+10), random.randint(self.top_right[1], self.top_right[1]+100))
        self.points = [self.top_left, self.bottom_left, self.bottom_right, self.top_right]