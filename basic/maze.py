from typing import Tuple, List, Optional
from collections import deque


class Maze:
    """
    Represent a rectangular maze with internal walls.
    """

    def __init__(self, width: int = 5, height: int = 5):
        """
        Initialize the maze with a given width and height.

        Args:
            width (int): Width of the maze.
            height (int): Height of the maze.
        """
        self._width = width
        self._height = height
        self._horizontal_walls = set()
        self._vertical_walls = set()

    @property
    def width(self) -> int:
        """Return the maze width."""
        return self._width

    @property
    def height(self) -> int:
        """Return the maze height."""
        return self._height

    def add_horizontal_wall(self, x_cordinates: int, horizontal_line: int):
        """
        Add an internal horizontal wall.

        Args:
            x_cordinates (int): X coordinate of the wall.
            horizontal_line (int): Y coordinate of the wall.
        """
        self._horizontal_walls.add((x_cordinates, horizontal_line))

    def add_vertical_wall(self, y_cordiates: int, vertical_line: int):
        """
        Add an internal vertical wall.

        Args:
            y_cordiates (int): Y coordinate of the wall.
            vertical_line (int): X coordinate of the wall.
        """
        self._vertical_walls.add((y_cordiates, vertical_line))

    def get_walls(
        self, x_cordinate: int, y_cordinate: int
    ) -> Tuple[bool, bool, bool, bool]:
        """
        Return the walls surrounding a cell.

        Args:
            x_cordinate (int): X coordinate of the cell.
            y_cordinate (int): Y coordinate of the cell.

        Returns:
            Tuple[bool, bool, bool, bool]: Walls in the order
            (north, east, south, west).
        """
        x = x_cordinate
        y = y_cordinate

        north = y == self._height - 1
        south = y == 0
        west = x == 0
        east = x == self._width - 1

        if (x, y + 1) in self._horizontal_walls:
            north = True

        if (x, y) in self._horizontal_walls:
            south = True

        if (y, x + 1) in self._vertical_walls:
            east = True

        if (y, x) in self._vertical_walls:
            west = True

        return north, east, south, west

    def sense_walls(self, runner):
        """
        Sense walls relative to the runner orientation.

        Args:
            runner (dict): Runner state.

        Returns:
            Tuple[bool, bool, bool]: Walls on the left, front, and right.
        """
        x = runner["x"]
        y = runner["y"]
        orient = runner["orientation"]

        walls = self.get_walls(x, y)

        side_map = {
            "N": (3, 0, 1),  # left=W, front=N, right=E
            "E": (0, 1, 2),  # left=N, front=E, right=S
            "S": (1, 2, 3),  # left=E, front=S, right=W
            "W": (2, 3, 0),  # left=S, front=W, right=N
        }

        left_i, front_i, right_i = side_map[orient]
        return walls[left_i], walls[front_i], walls[right_i]

    def go_straight(self, runner):
        """
        Move the runner forward by one cell.

        Args:
            runner (dict): Runner state.

        Returns:
            dict: Updated runner state.

        Raises:
            ValueError: If a wall blocks forward movement.
        """
        left, front, right = self.sense_walls(runner)

        if front:
            raise ValueError("Cannot go straight, wall in front of runne")

        x = runner["x"]
        y = runner["y"]
        orient = runner["orientation"]

        if orient == "N":
            y += 1
        elif orient == "S":
            y -= 1
        elif orient == "E":
            x += 1
        elif orient == "W":
            x -= 1

        return {"x": x, "y": y, "orientation": orient}

    def _turn(self, runner, direction: str):
        """
        Turn the runner left or right.

        Args:
            runner (dict): Runner state.
            direction (str): Turn direction.
        """
        orientations = ["N", "E", "S", "W"]
        current = runner["orientation"]
        idx = orientations.index(current)

        if direction == "Left":
            new_orientation = orientations[(idx - 1) % 4]
        elif direction == "Right":
            new_orientation = orientations[(idx + 1) % 4]
        else:
            raise ValueError("Direction must be left or right")

        return {
            "x": runner["x"],
            "y": runner["y"],
            "orientation": new_orientation,
        }

    def move(self, runner):
        """
        Move the runner using a left-hand rule.

        The runner first attempts to turn left and move forward.
        If that is not possible, it tries to move straight, then right.
        If all directions are blocked, it moves backward.
        """
        left_wall, front_wall, right_wall = self.sense_walls(runner)

        # Try to go left (turn left, then forward)
        if not left_wall:
            turned = self._turn(runner, "Left")
            new_runner = self.go_straight(turned)
            return new_runner, "LF"

        # Try to go straight
        if not front_wall:
            new_runner = self.go_straight(runner)
            return new_runner, "F"

        # Try to go right (turn right, then forward)
        if not right_wall:
            turned = self._turn(runner, "Right")
            new_runner = self.go_straight(turned)
            return new_runner, "RF"

        # Otherwise, go backward
        x = runner["x"]
        y = runner["y"]
        orient = runner["orientation"]
        opposite = {"N": "S", "S": "N", "E": "W", "W": "E"}[orient]

        if orient == "N":
            y -= 1
        elif orient == "S":
            y += 1
        elif orient == "E":
            x -= 1
        elif orient == "W":
            x += 1

        new_runner = {"x": x, "y": y, "orientation": opposite}
        return new_runner, "B"

    def explore(self, runner, goal=None):
        """
        Explore the maze until the goal is reached.

        Args:
            runner (dict): Initial runner state.
            goal (tuple, optional): Goal position.
        """
        if goal is None:
            goal = (self.width - 1, self.height - 1)

        log = []

        while (runner["x"], runner["y"]) != goal:
            new_runner, actions = self.move(runner)
            log.append((runner["x"], runner["y"], actions))
            runner = new_runner

        return log

    def _get_neighbours(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Return reachable neighbouring cells.

        Args:
            x (int): X coordinate.
            y (int): Y coordinate.
        """
        neighbours: List[Tuple[int, int]] = []

        north, east, south, west = self.get_walls(x, y)

        if not north and y + 1 < self.height:
            neighbours.append((x, y + 1))

        if not east and x + 1 < self.width:
            neighbours.append((x + 1, y))

        if not south and y - 1 >= 0:
            neighbours.append((x, y - 1))

        if not west and x - 1 >= 0:
            neighbours.append((x - 1, y))

        return neighbours

    def shortest_path(
        self,
        starting: Optional[Tuple[int, int]] = None,
        goal: Optional[Tuple[int, int]] = None,
    ) -> List[Tuple[int, int]]:
        """
        Compute the shortest path using breadth-first search.

        Args:
            starting (tuple, optional): Start position.
            goal (tuple, optional): Goal position.
        """
        if starting is None:
            start = (0, 0)
        else:
            start = starting

        if goal is None:
            target = (self.width - 1, self.height - 1)
        else:
            target = goal


        queue = deque()
        queue.append(start)

        visited = set()
        visited.add(start)

        parent: dict[Tuple[int, int], Tuple[int, int]] = {}

        found = False
        while queue:
            current = queue.popleft()
            if current == target:
                found = True
                break

            cx, cy = current
            for nx, ny in self._get_neighbours(cx, cy):
                neighbour = (nx, ny)
                if neighbour not in visited:
                    visited.add(neighbour)
                    parent[neighbour] = current
                    queue.append(neighbour)

        if not found:
            return []

        path: List[Tuple[int, int]] = []
        node = target
        while node != start:
            path.append(node)
            node = parent[node]
        path.append(start)

        path.reverse()
        return path
