"""Entry point to run GenerateMaze with arguments from the command line"""

import argparse
from generate_maze import GenerateMaze

parser = argparse.ArgumentParser()
parser.add_argument("--height", default=50, type=int)
parser.add_argument("--width", default=50, type=int)
parser.add_argument("--print-unsolved", action='store_true')
parser.add_argument("--print-solved", action='store_true')
parser.add_argument("--export-unsolved", action='store_true')
parser.add_argument("--export-solved", action='store_true')
parser.add_argument("--seed", default=None, type=int)
args = parser.parse_args()

maze = GenerateMaze(args.height, args.width, args.seed)

if args.print_unsolved:
    maze.print_pretty_unsolved_maze()

if args.print_solved:
    maze.print_pretty_solved_maze()

if args.export_unsolved:
    maze.export_unsolved_maze()

if args.export_solved:
    maze.export_solved_maze()
