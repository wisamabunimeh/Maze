'''Generate Maze module to generate mazes and solve them'''

import random
import sys
import numpy as np


class GenerateMaze:
    '''Generate a unicode based maze
       Prim's Algorithm is used to create the maze
       Depth First Search algorithm is used to solve the maze'''

    WALL = 'X'
    PATH = 'O'
    START = 'S'
    FINISH = 'F'
    SOLUTION = "W"
    VISITED = 'V'
    UNICODE_TEXT = {
        WALL: "\U00002B1B",  # Black
        PATH: "\U0001F7E6",  # Blue
        START: "\U0001F7E9",  # Green
        FINISH: "\U0001F7E5",  # Red
        VISITED: "\U0001F7E6",  # Blue
        SOLUTION: "\U0001F7E7"  # Orange
    }

    def __init__(self, height, width, seed=None):

        self.height = height
        self.width = width
        self.maze = []
        self.solved_maze = []
        self.start_coordinates = (0, 1)
        self.finish_coordinates = (self.height, self.width - 1)
        self.seed = self.__set_random_seed(seed)

        self.__generate_base_maze()
        self.__generate_maze()

        self.solved_maze = self.__solve_maze()

    def __set_random_seed(self, seed):
        '''If a seed set, the random number generated becomes
        deterministic. This allows mazes generated with the same
        height, width and seed to be identical'''
        if seed is None:
            seed = random.randrange(sys.maxsize)

        random.seed(seed)
        return seed

    def __print_maze(self, arr):
        '''Prints the a 2d-array to stdout'''

        for row in arr:
            string_row = ''.join(row)
            print(string_row)
        print("\n")

    def __pretty_maze(self, maze):
        '''Creates version of the maze with unicode emoji characters'''

        pretty_maze = maze.copy()
        for row, _ in enumerate(pretty_maze):
            for col, _ in enumerate(pretty_maze[row]):
                pretty_maze[row][col] = \
                    self.UNICODE_TEXT[pretty_maze[row][col]]
        return pretty_maze

    def print_pretty_unsolved_maze(self):
        '''Prints the unsolved maze with unicode emoji characters to the console'''

        pretty_unsolved_maze = self.__pretty_maze(self.maze)
        self.__print_maze(pretty_unsolved_maze)

    def print_pretty_solved_maze(self):
        """Prints the solved maze with unicode emoji characters to the console"""
        pretty_solved_maze = self.__pretty_maze(self.solved_maze)
        self.__print_maze(pretty_solved_maze)

    def export_unsolved_maze(self):
        '''Exports the unsolved maze as a text file'''

        pretty_unsolved_maze = self.__pretty_maze(self.maze)
        self.__export_maze(pretty_unsolved_maze, 'unsolved')

    def export_solved_maze(self):
        '''Exports the solved maze as a text file'''

        pretty_solved_maze = self.__pretty_maze(self.solved_maze)
        self.__export_maze(pretty_solved_maze, 'solved')

    def __export_maze(self, maze, kind):

        with open(f'{kind}-maze-{self.seed}.txt', 'w', encoding="utf8") \
                as file:
            for row in maze:
                file.write(''.join(row))
                file.write('\n')

    def __generate_base_maze(self):
        '''Creates an array with the perimeter blocked and,
        the starting and finishing points set'''

        self.height = self.height if self.height % 2 == 0 else self.height + 1
        self.width = self.width if self.width % 2 == 0 else self.width + 1

        self.maze = np.full(
            shape=(self.height + 1, self.width + 1),
            fill_value=self.WALL
        )

        self.maze[self.start_coordinates[0], self.start_coordinates[1]] = \
            self.START
        self.maze[self.height, self.width - 1] = self.FINISH

    def __get_walls(self, cell):
        '''Gets the neighboring walls of a cell,
        and returns the coordinates in an array'''

        walls = []
        if cell[0] + 1 < self.height:
            walls.append((cell[0] + 1, cell[1]))

        if cell[0] - 1 > 0:
            walls.append((cell[0] - 1, cell[1]))

        if cell[1] + 1 < self.width:
            walls.append((cell[0], cell[1] + 1))

        if cell[1] - 1 > 0:
            walls.append((cell[0], cell[1] - 1))

        return walls

    def __get_neighbors(self, arr, cell):
        '''Gets the neighboring neighbors (paths) of a cell,
        and returns the coordinates in an array'''

        neighbors = []
        if cell[0] + 2 < self.height and arr[cell[0] + 2][cell[1]] != \
           self.PATH:
            neighbors.append((cell[0] + 2, cell[1]))

        if cell[0] - 2 > 1 and arr[cell[0] - 2][cell[1]] != \
           self.PATH:
            neighbors.append((cell[0] - 2, cell[1]))

        if cell[1] + 2 < self.width and arr[cell[0]][cell[1] + 2] != self.PATH:
            neighbors.append((cell[0], cell[1] + 2))

        if cell[1] - 2 > 1 and arr[cell[0]][cell[1] - 2] != self.PATH:
            neighbors.append((cell[0], cell[1] - 2))

        return neighbors

    def __generate_maze(self):
        '''Iterative implementation of Prim's algorithm to generate all
        the possible paths within the maze'''

        neighbors = []
        walls = []

        self.maze[1][1] = self.PATH
        current_cell = (1, 1)
        neighbors = neighbors + self.__get_neighbors(self.maze, current_cell)
        walls = walls + self.__get_walls(current_cell)

        while len(neighbors) > 0:
            neighbor = random.choice(neighbors)
            neighbor_walls = self.__get_walls(neighbor)
            intersect = []

            for neighbor_wall in neighbor_walls:
                if neighbor_wall in walls:
                    intersect.append(neighbor_wall)

            random_wall = random.choice(intersect)
            neighbor_walls.remove(random_wall)

            self.maze[random_wall[0]][random_wall[1]] = self.PATH

            self.maze[random_wall[0]][random_wall[1]] = self.PATH
            self.maze[neighbor[0]][neighbor[1]] = self.PATH

            neighbors = neighbors + self.__get_neighbors(self.maze, neighbor)
            walls = walls + neighbor_walls
            walls.remove(random_wall)
            neighbors.remove(neighbor)
            neighbors = list(set(neighbors))

    def __potential_paths(self, arr, current_cell):
        '''Gets the possible paths from a cell and return
        the coordinates in an array'''

        potential_paths = []
        if arr[current_cell[0] + 1, current_cell[1]] in \
           {self.PATH, self.FINISH}:
            potential_paths.append((current_cell[0] + 1, current_cell[1]))

        if arr[current_cell[0] - 1, current_cell[1]] in \
           {self.PATH, self.FINISH}:
            potential_paths.append((current_cell[0] - 1, current_cell[1]))

        if arr[current_cell[0], current_cell[1] + 1] in \
           {self.PATH, self.FINISH}:
            potential_paths.append((current_cell[0], current_cell[1] + 1))

        if arr[current_cell[0], current_cell[1] - 1] in \
           {self.PATH, self.FINISH}:
            potential_paths.append((current_cell[0], current_cell[1] - 1))

        return potential_paths

    def __solve_maze(self):
        '''Iterative implementation of depth-first search algorithm
        to generate find the path from the starting point to the
        finishing point'''

        self.solved_maze = self.maze.copy()
        solution_path = []
        current_cell = (1, 1)

        solution_path.append(current_cell)
        while len(solution_path) > 0:
            current_cell = solution_path[-1]

            if self.solved_maze[current_cell[0], current_cell[1]] == \
               self.FINISH:
                break

            if self.solved_maze[current_cell[0], current_cell[1]] == self.WALL:
                solution_path.pop()
                continue

            potenential_paths = \
                self.__potential_paths(self.solved_maze, current_cell)

            if len(potenential_paths) == 0:
                self.solved_maze[current_cell[0], current_cell[1]] = \
                    self.VISITED
                solution_path.pop()
            else:
                solution_path = solution_path + potenential_paths
                self.solved_maze[current_cell[0], current_cell[1]] = \
                    self.SOLUTION

        return self.solved_maze
