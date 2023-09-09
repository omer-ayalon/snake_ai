import copy
import random
import sys
from os import environ

environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame

pygame.display.set_caption('Hamiltonian Path Generator')

pygame.init()

fps = 20
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

grid_shape = [5, 5]

Font = pygame.font.SysFont('timesnewroman', 30)


class Maze:
    def __init__(self, shape):
        self.grid_visited = [[0 for _ in range(grid_shape[1])] for _ in range(grid_shape[0])]
        self.grid_edges = [[{'right': True, 'down': True, 'left': True, 'up': True} for _ in range(grid_shape[1])]
                           for _ in range(grid_shape[0])]
        self.grid_shape = shape
        self.current_pos = [0, 0]
        self.visited_num = 0
        self.done = False
        self.visited_stack = []

    def generate_maze(self):
        while not self.done:
            self.step()

    def step(self):
        self.visited_stack.append(self.current_pos)
        self.grid_visited[self.current_pos[0]][self.current_pos[1]] = 1

        neighbors = self.get_neighbors(self.current_pos)

        if len(neighbors) > 0:
            rand = random.choice(neighbors)
            dy, dx = (rand[0] - self.current_pos[0]), (rand[1] - self.current_pos[1])

            if dy == 1:
                self.grid_edges[self.current_pos[0]][self.current_pos[1]]['down'] = False
                self.grid_edges[self.current_pos[0] + 1][self.current_pos[1]]['up'] = False
            if dy == -1:
                self.grid_edges[self.current_pos[0]][self.current_pos[1]]['up'] = False
                self.grid_edges[self.current_pos[0] - 1][self.current_pos[1]]['down'] = False
            if dx == 1:
                self.grid_edges[self.current_pos[0]][self.current_pos[1]]['right'] = False
                self.grid_edges[self.current_pos[0]][self.current_pos[1] + 1]['left'] = False
            if dx == -1:
                self.grid_edges[self.current_pos[0]][self.current_pos[1]]['left'] = False
                self.grid_edges[self.current_pos[0]][self.current_pos[1] - 1]['right'] = False

            self.current_pos = rand
            self.visited_num += 1

        else:
            a = []
            for i in range(grid_shape[1]):
                a.append(all(self.grid_visited[i]) == 1)
            if all(a) == 1:
                self.done = True
            else:
                while len(neighbors) == 0:
                    self.current_pos = self.visited_stack.pop()
                    neighbors = self.get_neighbors(self.current_pos)

    def get_neighbors(self, pos):
        arr = []
        if pos[0] > 0:
            if not self.grid_visited[pos[0] - 1][pos[1]]:  # Check Up
                arr.append([pos[0] - 1, pos[1]])
        if pos[1] < grid_shape[1] - 1:
            if not self.grid_visited[pos[0]][pos[1] + 1]:  # Check Right
                arr.append([pos[0], pos[1] + 1])
        if pos[0] < grid_shape[0] - 1:
            if not self.grid_visited[pos[0] + 1][pos[1]]:  # Check Down
                arr.append([pos[0] + 1, pos[1]])
        if pos[1] > 0:
            if not self.grid_visited[pos[0]][pos[1] - 1]:  # Check Left
                arr.append([pos[0], pos[1] - 1])

        return arr

    def draw(self):
        for j in range(grid_shape[1]):
            for i in range(grid_shape[0]):
                if self.grid_visited[i][j]:
                    pygame.draw.rect(screen, (255, 255, 255), [j * width / grid_shape[1],
                                                               i * height / grid_shape[0],
                                                               width / grid_shape[1] + 1,
                                                               height / grid_shape[0] + 1])

                if self.grid_edges[i][j]['down']:
                    pygame.draw.line(screen, (0, 0, 0), [width / grid_shape[1] * j, height / grid_shape[0] * (i + 1)],
                                     [width / grid_shape[1] * (j + 1), height / grid_shape[0] * (i + 1)], 10)
                if self.grid_edges[i][j]['right']:
                    pygame.draw.line(screen, (0, 0, 0), [width / grid_shape[1] * (j + 1), height / grid_shape[0] * i],
                                     [width / grid_shape[1] * (j + 1), height / grid_shape[0] * (i + 1)], 10)

                if not self.done:
                    pygame.draw.rect(screen, (0, 255, 0), [self.current_pos[1] * width / grid_shape[1],
                                                           self.current_pos[0] * height / grid_shape[0],
                                                           width / grid_shape[1] + 1,
                                                           height / grid_shape[0] + 1])


class Path:
    def __init__(self):
        self.dir = 'right'
        self.current_cell = [0, 0]
        self.path = [[0, 0]]
        self.possible_dirs = {'right': [0, 1], 'down': [1, 0], 'left': [0, -1], 'up': [-1, 0]}
        self.follow_wall = 'up'
        self.grid_edges = [
            [{'right': False, 'down': False, 'left': False, 'up': False} for _ in range(grid_shape[1] * 2)]
            for _ in range(grid_shape[0] * 2)]
        self.make_edges()
        self.done = False

    def make_edges(self):
        for i in range(grid_shape[0]):
            for j in range(grid_shape[1]):
                for turn in ['right', 'down', 'left', 'up']:
                    if maze.grid_edges[i][j][turn]:
                        if turn == 'right':
                            self.grid_edges[i * 2][j * 2 + 1][turn] = True
                            self.grid_edges[i * 2 + 1][j * 2 + 1][turn] = True
                        if turn == 'down':
                            self.grid_edges[i * 2 + 1][j * 2][turn] = True
                            self.grid_edges[i * 2 + 1][j * 2 + 1][turn] = True
                        if turn == 'left':
                            self.grid_edges[i * 2][j * 2][turn] = True
                            self.grid_edges[i * 2 + 1][j * 2][turn] = True
                        if turn == 'up':
                            self.grid_edges[i * 2][j * 2][turn] = True
                            self.grid_edges[i * 2][j * 2 + 1][turn] = True

    def move(self):
        self.current_cell[0] += self.possible_dirs[self.dir][0]
        self.current_cell[1] += self.possible_dirs[self.dir][1]
        self.path.append(copy.deepcopy(self.current_cell))

    def step(self):
        if not self.done:
            if len(self.path) > 1 and self.path[0] == self.path[-1]:
                self.done = True
                del self.path[-1]

            if self.grid_edges[self.current_cell[0]][self.current_cell[1]][self.follow_wall]:
                if not self.grid_edges[self.current_cell[0]][self.current_cell[1]][self.dir]:
                    self.move()
                else:
                    for i, dir in enumerate(self.possible_dirs):
                        if not self.grid_edges[self.current_cell[0]][self.current_cell[1]][dir]:
                            if dir != self.dir:
                                self.dir = dir
                                self.follow_wall = list(self.possible_dirs.keys())[(i - 1) % 4]
                                break
            else:
                self.dir = copy.deepcopy(self.follow_wall)
                idx = (list((self.possible_dirs.keys())).index(self.dir) - 1)
                self.follow_wall = list(self.possible_dirs.keys())[idx % 4]
                self.move()

    def draw(self):
        for i, pos in enumerate(self.path):
            idx_num = Font.render(str(self.path.index(pos)), True, (0, 255, 0))
            screen.blit(idx_num, (pos[1] * width / grid_shape[1] / 2 + width / grid_shape[1] / 6,
                                  pos[0] * height / grid_shape[0] / 2 + height / grid_shape[0] / 8))

        for i in range(grid_shape[1] * 2):
            for j in range(grid_shape[0] * 2):
                pygame.draw.line(screen, (255, 0, 0), [j * width / grid_shape[1] / 2, 0],
                                 [j * width / grid_shape[1] / 2, height], 1)
                pygame.draw.line(screen, (255, 0, 0), [0, i * height / grid_shape[0] / 2],
                                 [width, i * height / grid_shape[0] / 2], 1)


maze = Maze(shape=grid_shape)
path = Path()

while True:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()

    maze.draw()

    if not maze.done:
        maze.step()
        if maze.done:
            path.__init__()
    else:
        if not path.done:
            path.step()
        path.draw()

    pygame.display.flip()
    fpsClock.tick(fps)
