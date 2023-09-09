import copy
import random
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.init()

fps = 5
fpsClock = pygame.time.Clock()

screen_width, screen_height = 640, 480
screen = pygame.display.set_mode((screen_width, screen_height))

num_cell = 10

dirs_dict = {'right': [0, 1], 'down': [1, 0], 'left': [0, -1], 'up': [-1, 0]}


class Snake:
    def __init__(self):
        self.score = 0
        self.snake_list = [{'pos': [0, 1], 'dir': 'right', 'moving': True},
                           {'pos': [0, 0], 'dir': 'right', 'moving': True}]
        self.food_pos = []
        self.adding_cube = None
        self.dir = 'right'
        self.turns = []
        self.game_over = False
        self.generate_food()

    def step(self):
        self.keyboard_handler()
        if not self.game_over:
            self.move()
            self.snake_list[-1]['moving'] = True
            self.check_food_eaten()
            self.check_game_over()

    def check_food_eaten(self):
        if self.food_pos == self.snake_list[0]['pos']:
            self.snake_list.append(copy.deepcopy(self.snake_list[-1]))
            self.snake_list[-1]['moving'] = False
            self.generate_food()
            self.score += 1

    def generate_food(self):
        # Generate Food Position Omitting Body Positions
        choices = [[pos1, pos2] for pos1 in range(num_cell) for pos2 in range(num_cell)]
        for cube in self.snake_list:
            if cube['pos'] in choices:
                choices.remove(cube['pos'])

        self.food_pos = random.choice(choices)

    def move(self):
        # Check If A Turn Needs To Be Done And Move In Direction
        for i, cube in enumerate(self.snake_list):
            for j, turn in enumerate(self.turns):
                if cube['pos'] == turn['pos']:
                    cube['dir'] = turn['dir']
                    if i == len(self.snake_list)-1:
                        del self.turns[j]

            if cube['moving']:
                cube['pos'][0] += dirs_dict[cube['dir']][0]
                cube['pos'][1] += dirs_dict[cube['dir']][1]

    def check_game_over(self):
        # Check If Head Collide With The Body
        for cube in self.snake_list[1:]:
            if self.snake_list[0]['pos'] == cube['pos']:
                self.game_over = True

        # Check If Head Is Outside The Screen
        if (self.snake_list[0]['pos'][0] < 0 or self.snake_list[0]['pos'][0] > num_cell - 1) or (
                self.snake_list[0]['pos'][1] < 0 or self.snake_list[0]['pos'][1] > num_cell - 1):
            self.game_over = True

    def keyboard_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if not self.game_over:
                    if event.key == pygame.K_RIGHT:
                        self.turns.append(
                            {'pos': copy.deepcopy(self.snake_list[0]['pos']), 'dir': 'right', 'moving': False})
                    if event.key == pygame.K_DOWN:
                        self.turns.append(
                            {'pos': copy.deepcopy(self.snake_list[0]['pos']), 'dir': 'down', 'moving': False})
                    if event.key == pygame.K_LEFT:
                        self.turns.append(
                            {'pos': copy.deepcopy(self.snake_list[0]['pos']), 'dir': 'left', 'moving': False})
                    if event.key == pygame.K_UP:
                        self.turns.append(
                            {'pos': copy.deepcopy(self.snake_list[0]['pos']), 'dir': 'up', 'moving': False})

    def draw(self):
        # Draw Snake
        for i, cube in enumerate(self.snake_list):
            if i == 0:
                color = (255, 0, 0)
            else:
                color = (0, 255, 0)
            pygame.draw.rect(screen, color, [cube['pos'][1] * screen_width / num_cell,
                                             cube['pos'][0] * screen_height / num_cell,
                                             screen_width / num_cell,
                                             screen_height / num_cell])

        # Draw Lines
        for i in range(num_cell + 1):
            pygame.draw.line(screen, (255, 255, 255), [i * screen_width / num_cell, 0],
                             [i * screen_width / num_cell, screen_height])
            pygame.draw.line(screen, (255, 255, 255), [0, i * screen_height / num_cell],
                             [screen_width, i * screen_height / num_cell])

        # Draw Food
        pygame.draw.circle(screen, (0, 0, 255),
                           [self.food_pos[1] * screen_width / num_cell + screen_width / num_cell / 2,
                            self.food_pos[0] * screen_height / num_cell + screen_height / num_cell / 2], 5)


game = Snake()

while True:
    screen.fill((0, 0, 0))

    game.step()
    game.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
