import pygame
import os


class Screen:
    def __init__(self, constants):
        self.constants = constants
        self.screen = self.setup_screen()
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.clock = pygame.time.Clock()


    def setup_screen(self):
        screen = pygame.display.set_mode((self.constants.WORLD_WIDTH, self.constants.WORLD_HEIGHT))
        pygame.display.set_caption('Evolution')
        return screen

    def update_display(self, best_robot, timestep, food, population, generation):
        self.screen.fill(self.constants.BACKGROUND_COLOR)

        self.draw_food(food)
        for agent in population:
            if not agent.out_of_bounds:
                for coord in agent.sensing_rects_before_move:
                    rect = pygame.Rect(coord[0], coord[1], self.constants.SCALE_FACTOR, self.constants.SCALE_FACTOR)
                    rect.center = coord
                    pygame.draw.rect(self.screen, (0, 0, 100), rect, 1)

                agent_img = pygame.image.load('/Users/emilknudsen/Desktop/research/sheep.png').convert_alpha()
                agent_img = pygame.transform.scale(agent_img, (self.constants.SCALE_FACTOR, self.constants.SCALE_FACTOR))
                self.screen.blit(agent_img, agent.get_rect())
                #pygame.draw.rect(self.screen, agent.color, agent.get_rect())
                # for coord in agent.py.sensing_rects_after_move:
                #     rect = pygame.Rect(coord[0], coord[1], SCALE_FACTOR, SCALE_FACTOR)
                #     rect.center = coord
                #     pygame.draw.rect(self.screen, (100, 0, 0), rect, 2)
                # for coord in agent.py.previous_positions.queue:
                #     rect = pygame.Rect(coord[0], coord[1], SCALE_FACTOR, SCALE_FACTOR)
                #     rect.center = coord
                #     pygame.draw.rect(self.screen, agent.py.color, rect)
        self.draw_background_lines()
        self.update_text(best_robot, timestep, population, food, generation)
        self.clock.tick()
        pygame.display.update()

    def draw_background_lines(self):
        for i in range(0, self.constants.WORLD_WIDTH, self.constants.SCALE_FACTOR):
            pygame.draw.line(self.screen, self.constants.LINE_COLOR, (i+self.constants.SCALE_FACTOR/2, 0), (i+self.constants.SCALE_FACTOR/2, self.constants.WORLD_HEIGHT), 1)

        for j in range(0, self.constants.WORLD_HEIGHT, self.constants.SCALE_FACTOR):
            pygame.draw.line(self.screen, self.constants.LINE_COLOR, (0, j+self.constants.SCALE_FACTOR/2), (self.constants.WORLD_WIDTH, j+ self.constants.SCALE_FACTOR/2), 1)


    def draw_food(self, food):
        for f in food.items():
            # if f.energy < 40:
            #     pygame.draw.rect(self.screen, FOOD_COLOR, f.get_rect())
            # else:
            pygame.draw.circle(self.screen, self.constants.FOOD_COLOR, (f[1].x, f[1].y),
                               self.constants.SCALE_FACTOR / 2 - 2)
            # pygame.draw.rect(self.screen, self.constants.FOOD_COLOR, f[1].get_rect())

    def draw_water(self):
        for w in self.water:
            pygame.draw.rect(self.screen, self.constants.WATER_COLOR, w)

    def update_text(self, best_robot, timestep, population, food, generation):
        text = self.font.render("Timestep: " + str(timestep), True, self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 20
        self.screen.blit(text, text_rect)

        text = self.font.render("Energy for best robot: " + str(best_robot.energy.__round__(1)), True,
                                self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 40
        self.screen.blit(text, text_rect)

        text = self.font.render("Fitness for best robot: " + str(best_robot.genome.fitness.__round__(1)), True,
                                self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 60
        self.screen.blit(text, text_rect)

        text = self.font.render("Robots: " + str(len(list(filter(lambda agent: not agent.out_of_bounds, population)))),
                                True, self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 80
        self.screen.blit(text, text_rect)

        text = self.font.render("Food: " + str(len(food)), True, self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 100
        self.screen.blit(text, text_rect)

        text = self.font.render("Generation: " + str(generation), True, self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 120
        self.screen.blit(text, text_rect)

        text = self.font.render("FPS: " + str(self.clock.get_fps().__round__(1)), True, self.constants.TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = self.constants.WORLD_WIDTH - 100, 20
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 0, 0), (
            best_robot.get_rect().topleft[0] - 7.5, best_robot.get_rect().topleft[1] - 7.5,
            self.constants.SCALE_FACTOR + 15, self.constants.SCALE_FACTOR + 15), 2, border_radius=1)
