'''Tests for GenerateMaze'''

import io
import os
import sys
import unittest
from generate_maze import GenerateMaze


class TestGenerateMaze(unittest.TestCase):
    '''Test class for GenerateMaze'''

    def test_print_pretty_unsolved_maze(self):
        '''Tests the a pretty unsolved maze is generated and printed to the console'''

        expected_unsolved_maze = '⬛🟩⬛⬛⬛⬛⬛⬛⬛⬛⬛\n' + \
                                 '⬛🟦🟦🟦🟦🟦🟦🟦🟦🟦⬛\n' + \
                                 '⬛🟦⬛⬛⬛🟦⬛🟦⬛⬛⬛\n' + \
                                 '⬛🟦⬛🟦🟦🟦⬛🟦🟦🟦⬛\n' + \
                                 '⬛🟦⬛⬛⬛⬛⬛⬛⬛⬛⬛\n' + \
                                 '⬛🟦🟦🟦⬛🟦⬛🟦⬛🟦⬛\n' + \
                                 '⬛⬛⬛🟦⬛🟦⬛🟦⬛🟦⬛\n' + \
                                 '⬛🟦🟦🟦🟦🟦🟦🟦🟦🟦⬛\n' + \
                                 '⬛🟦⬛🟦⬛⬛⬛🟦⬛🟦⬛\n' + \
                                 '⬛🟦⬛🟦⬛🟦🟦🟦⬛🟦⬛\n' + \
                                 '⬛⬛⬛⬛⬛⬛⬛⬛⬛🟥⬛\n\n\n'

        stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        maze = GenerateMaze(10, 10, 1)
        maze.print_pretty_unsolved_maze()

        printed_maze = new_stdout.getvalue()
        sys.stdout = stdout

        self.assertEqual(printed_maze, expected_unsolved_maze)

    def test_print_pretty_solved_maze(self):
        '''Tests the a pretty solved maze is generated and printed to the console'''

        expected_solved_maze = '⬛🟩⬛⬛⬛⬛⬛⬛⬛⬛⬛\n' + \
                               '⬛🟧🟦🟦🟦🟦🟦🟦🟦🟦⬛\n' + \
                               '⬛🟧⬛⬛⬛🟦⬛🟦⬛⬛⬛\n' + \
                               '⬛🟧⬛🟦🟦🟦⬛🟦🟦🟦⬛\n' + \
                               '⬛🟧⬛⬛⬛⬛⬛⬛⬛⬛⬛\n' + \
                               '⬛🟧🟧🟧⬛🟦⬛🟦⬛🟦⬛\n' + \
                               '⬛⬛⬛🟧⬛🟦⬛🟦⬛🟦⬛\n' + \
                               '⬛🟦🟦🟧🟧🟧🟧🟧🟧🟧⬛\n' + \
                               '⬛🟦⬛🟦⬛⬛⬛🟦⬛🟧⬛\n' + \
                               '⬛🟦⬛🟦⬛🟦🟦🟦⬛🟧⬛\n' + \
                               '⬛⬛⬛⬛⬛⬛⬛⬛⬛🟥⬛\n\n\n'

        stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        maze = GenerateMaze(10, 10, 1)
        maze.print_pretty_solved_maze()

        printed_maze = new_stdout.getvalue()
        sys.stdout = stdout

        self.assertEqual(printed_maze, expected_solved_maze)

    def test_export_unsolved_maze(self):
        '''Tests the a pretty unsolved maze is generated and exported'''

        maze = GenerateMaze(10, 10, 1)
        maze.export_unsolved_maze()

        maze_file_fixture_path = os.path.abspath(os.path.dirname(__file__)) + \
            '/fixtures/unsolved-maze-1.txt'
        generated_maze_file_path = os.getcwd() + '/unsolved-maze-1.txt'

        with io.open(generated_maze_file_path, encoding="utf8") as generated_file:
            generated_maze_file_content = list(generated_file)

        with io.open(maze_file_fixture_path, encoding="utf8") as maze_file_fixture_file:
            maze_fixture_file_content = list(maze_file_fixture_file)

        self.assertListEqual(
            generated_maze_file_content,
            maze_fixture_file_content,
            "generated unsolved maze file does not match expected fixture file"
        )

        os.remove(generated_maze_file_path)

    def test_export_solved_maze(self):
        '''Tests the a pretty solved maze is generated and exported'''

        maze = GenerateMaze(10, 10, 1)
        maze.export_solved_maze()

        maze_file_fixture_path = os.path.abspath(os.path.dirname(__file__)) + \
            '/fixtures/solved-maze-1.txt'
        generated_maze_file_path = os.getcwd() + '/solved-maze-1.txt'

        with io.open(generated_maze_file_path, encoding="utf8") as generated_file:
            generated_maze_file_content = list(generated_file)

        with io.open(maze_file_fixture_path, encoding="utf8") as maze_file_fixture_file:
            maze_fixture_file_content = list(maze_file_fixture_file)

        os.remove(generated_maze_file_path)

        self.assertListEqual(
            generated_maze_file_content,
            maze_fixture_file_content,
            "generated solved maze file does not match expected fixture file"
        )

    def test_starting_cell(self):
        '''Tests the starting point is the correct coordinate'''

        generated_maze = GenerateMaze(10, 10)

        self.assertEqual(generated_maze.maze[0][1], 'S', "incorrect starting point")

    def test_finishing_cell(self):
        '''Tests the finishing point is the correct coordinate'''

        generated_maze = GenerateMaze(10, 10)

        self.assertEqual(generated_maze.maze[10][9], 'F', "incorrect finishing point")


unittest.main()
