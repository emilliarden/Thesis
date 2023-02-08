import random
import neat
import pygame

from Simple.Classes.food import Food
from Simple.Classes.agent import Agent
from Simple.Classes.constants import SCALE_FACTOR, WORLD_HEIGHT, WORLD_WIDTH, WATER_COLOR, FOOD_COLOR, FOOD2_COLOR,\
    TEXT_COLOR, BACKGROUND_COLOR, INITIAL_POPULATION_SIZE, INITIAL_AMOUNT_FOOD


class Simulation:
    def __init__(self, config):
        pygame.init()
        self.screen = self.setup_screen()
        self.neat_population = None
        self.water = []
        self.food = Food.create_food(self.water)
        self.population = None
        self.timestep = 0
        self.clock = pygame.time.Clock()
        self.config = config
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.current_best_robot = None


    def setup_screen(self):
        screen = pygame.display.set_mode((WORLD_WIDTH, WORLD_HEIGHT))
        pygame.display.set_caption('Evolution')
        return screen


    def create_population_from_genomes(self, genomes):
        agents = []
        for i, (genome_id, genome) in enumerate(genomes):
            agent = Agent()
            agent.x = 40 * i
            agent.y = WORLD_HEIGHT / 2
            agent.q = random.random()
            agent.genome = genome
            agent.genome.fitness = 0
            agent.nn = neat.nn.FeedForwardNetwork.create(genome, config)
            agents.append(agent)
        return agents

    def reset_for_next_gen(self, genomes):
        self.food = Food.create_food(self.water)
        self.population = self.create_population_from_genomes(genomes)
        self.timestep = 0
        self.timesteps_without_progress = 0

    def simulate(self, genomes, draw: bool = True):
        self.reset_for_next_gen(genomes)

        while self.timestep < 5000 and self.timesteps_without_progress < 500:
            self.timestep += 1
            # TO QUIT PYGAME
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()

            #SIMULATION
            for agent in self.population:
                if agent.out_of_bounds:
                    continue

                new_pos = agent.move(self)

                #HITS FOOD
                if new_pos in self.food:
                    self.timesteps_without_progress = 0
                    #agent.energy += self.food[new_pos].energy
                    agent.genome.fitness += self.food[new_pos].energy
                    self.food.pop(new_pos)

                list_without_self = list(self.population)
                list_without_self.remove(agent)

                #HITS OTHER ROBOT OR OUT OF BOUNDS
                if (new_pos in set([a.get_center_coord() for a in list_without_self])) or new_pos[0] > WORLD_WIDTH or new_pos[0] < 0 or new_pos[1] > WORLD_HEIGHT or new_pos[1] < 0:
                    agent.out_of_bounds = True
                    continue


            self.timesteps_without_progress += 1

            if draw or self.neat_population.generation > 475:
                rank_of_robots = sorted(self.population, key=lambda x: x.genome.fitness, reverse=True)
                best_robot = rank_of_robots[0] if len(rank_of_robots) > 0 else Agent()
                self.update_display(best_robot)

    def update_display(self, best_robot):
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_food()
        for agent in self.population:
            if not agent.out_of_bounds:
                pygame.draw.rect(self.screen, agent.color, agent.get_rect())
        self.update_text(best_robot)
        self.clock.tick()
        pygame.display.update()


    def draw_food(self):
        for f in self.food.items():
            # if f.energy < 40:
            #     pygame.draw.rect(self.screen, FOOD_COLOR, f.get_rect())
            # else:
            pygame.draw.rect(self.screen, FOOD_COLOR, f[1].get_rect())

    def draw_water(self):
        for w in self.water:
            pygame.draw.rect(self.screen, WATER_COLOR, w)

    def update_text(self, best_robot):
        text = self.font.render("Timestep: " + str(self.timestep), True, TEXT_COLOR )
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 20
        self.screen.blit(text, text_rect)

        text = self.font.render("Energy for best robot: " + str(best_robot.genome.fitness), True, TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 40
        self.screen.blit(text, text_rect)

        text = self.font.render("Robots: " + str(len(self.population)), True, TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 60
        self.screen.blit(text, text_rect)

        text = self.font.render("Food: " + str(len(self.food)), True, TEXT_COLOR)
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 80
        self.screen.blit(text, text_rect)

        text = self.font.render("Generation: " + str(self.neat_population.generation), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.bottomleft = 0, 100
        self.screen.blit(text, text_rect)

        text = self.font.render("FPS: " + str(self.clock.get_fps().__round__(1)), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.bottomleft = WORLD_WIDTH-100, 20
        self.screen.blit(text, text_rect)

        pygame.draw.rect(self.screen, (255, 0, 0), (best_robot.get_rect().topleft[0]-7.5, best_robot.get_rect().topleft[1]-7.5, SCALE_FACTOR+15, SCALE_FACTOR+15), 2, border_radius=1)

    def eval_genomes(self, genomes, config):
        self.simulate(genomes, False)


    def run_neat(self):
        #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-20')
        self.neat_population = neat.Population(self.config)
        self.neat_population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        self.neat_population.add_reporter(stats)
        self.neat_population.add_reporter(neat.Checkpointer(100))
        winner = self.neat_population.run(self.eval_genomes, 500)
        print(winner)


if __name__ == "__main__":
    config_path = "/Users/emilknudsen/Desktop/research/Simple/config.txt"
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    simulation = Simulation(config)
    simulation.run_neat()
