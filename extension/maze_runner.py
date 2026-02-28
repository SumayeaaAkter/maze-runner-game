"""
Maze runner application entry point.

Reads an ASCII maze file, explores the maze using a runner,
computes the shortest path, and writes results to output files.
"""

from __future__ import annotations

import argparse
import sys
import csv
from typing import Tuple, List

from maze import Maze
from runner import create_runner


def maze_reader(maze_file: str) -> Maze:
    """
    Read an ASCII maze file and construct a Maze object.

    Args:
        maze_file (str): Path to the maze file.

    Returns:
        Maze: Constructed maze object.

    Raises:
        IOError: If the maze file cannot be read.
        ValueError: If the maze format is invalid.
    """
    try:
        with open(maze_file, "r") as f:
            rows = [line.rstrip("\n") for line in f]
    except Exception as exc:
        raise IOError(f"Failed to read maze file '{maze_file}'") from exc

    if not rows:
        raise ValueError("Maze file is empty")

    ascii_height = len(rows)
    ascii_width = len(rows[0])

    for line in rows:
        if len(line) != ascii_width:
            raise ValueError("Maze rows have inconsistent widths")

    if (ascii_height - 1) % 2 != 0 or (ascii_width - 1) % 2 != 0:
        raise ValueError("Maze dimensions must be odd sized ASCII layout")

    maze_height = (ascii_height - 1) // 2
    maze_width = (ascii_width - 1) // 2

    if not all(c == "#" for c in rows[0]):
        raise ValueError("Top border must be all '#'")
    if not all(c == "#" for c in rows[-1]):
        raise ValueError("Bottom border must be all '#'")
    for r in rows:
        if r[0] != "#" or r[-1] != "#":
            raise ValueError("Side borders must be '#'")

    maze = Maze(maze_width, maze_height)

    for y in range(maze_height):
        for x in range(maze_width):
            ascii_x = 2 * x + 1
            ascii_y = 2 * (maze_height - 1 - y) + 1

            if x < maze_width - 1:
                if rows[ascii_y][ascii_x + 1] == "#":
                    maze.add_vertical_wall(y, x + 1)

            if y < maze_height - 1:
                if rows[ascii_y - 1][ascii_x] == "#":
                    maze.add_horizontal_wall(x, y + 1)

    return maze


def parse_coord(s: str) -> Tuple[int, int]:
    """
    Parse a coordinate string in the form "x,y".

    Args:
        s (str): Coordinate string.

    Returns:
        Tuple[int, int]: Parsed (x, y) coordinates.

    Raises:
        ValueError: If the format is invalid.
    """
    try:
        a, b = s.split(",")
        return int(a.strip()), int(b.strip())
    except Exception as exc:
        raise ValueError(
            f"Invalid coordinate format: '{s}' (expected x,y)"
        ) from exc


def write_exploration_log(
    filename: str, exploration_log: List[Tuple[int, int, str]]
):
    """
    Write the exploration log to a CSV file.

    Args:
        filename (str): Output CSV filename.
        exploration_log (list): Exploration log entries.
    """
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Step", "x-coordinate", "y-coordinate", "Actions"])
        for step, (x, y, actions) in enumerate(exploration_log, start=1):
            writer.writerow([step, x, y, actions])


def write_statistics(
    filename: str,
    maze_file: str,
    exploration_steps: int,
    shortest_path: List[Tuple[int, int]],
):
    """
    Write exploration statistics to a text file.

    Args:
        filename (str): Output filename.
        maze_file (str): Maze file name.
        exploration_steps (int): Number of exploration steps.
        shortest_path (list): Shortest path coordinates.
    """
    path_length = len(shortest_path)
    score = exploration_steps / 4 + path_length

    with open(filename, "w") as f:
        f.write(f"{maze_file}\n")
        f.write(f"{score}\n")
        f.write(f"{exploration_steps}\n")
        f.write(f"{shortest_path}\n")
        f.write(f"{path_length}\n")


def main():
    """
    Parse arguments, run the maze exploration, and output results.
    """
    parser = argparse.ArgumentParser(description="ECS Maze Runner")

    parser.add_argument("maze", help="Maze filename, e.g., maze1.mz")
    parser.add_argument("--starting", help='Start position "x,y"', default=None)
    parser.add_argument("--goal", help='Goal position "x,y"', default=None)

    args = parser.parse_args()

    try:
        maze = maze_reader(args.maze)

        start = parse_coord(args.starting) if args.starting else None
        goal = parse_coord(args.goal) if args.goal else None

        if start:
            x, y = start
            if not (0 <= x < maze.width and 0 <= y < maze.height):
                raise ValueError(f"Starting position {start} is outside the maze")

        if goal:
            x, y = goal
            if not (0 <= x < maze.width and 0 <= y < maze.height):
                raise ValueError(f"Goal position {goal} is outside the maze")

        runner_start_x, runner_start_y = start if start else (0, 0)
        runner = create_runner(runner_start_x, runner_start_y, "N")

        exploration_log = maze.explore(runner, goal)
        exploration_steps = len(exploration_log)

        write_exploration_log("exploration.csv", exploration_log)

        shortest = maze.shortest_path(start, goal)

        write_statistics("statistics.txt", args.maze, exploration_steps, shortest)

        print("Shortest path:", shortest)

    except (IOError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
