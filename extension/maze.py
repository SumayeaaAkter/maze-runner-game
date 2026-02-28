from typing import Tuple, List, Optional


class Maze:
    """
    Represent a rectangular maze with internal walls.

    The maze supports runner movement, wall sensing, exploration,
    and shortest-path computation using search algorithms.
    """

    def __init__(self, width: int = 5, height: int = 5):
        """
        Initialize the maze with a given width and height.
        """
        self._width = width
        self._height = height

        self._horizontal_walls = set()
        self._vertical_walls = set()

    @property
    def width(self) -> int:
        """Return the width of the maze."""
        return self._width

    @property
    def height(self) -> int:
        """Return the height of the maze."""
        return self._height

    def add_horizontal_wall(self, x_cordinates: int, horizontal_line: int):
        """
        Add an internal horizontal wall to the maze.
        """
        self._horizontal_walls.add((x_cordinates, horizontal_line))

    def add_vertical_wall(self, y_cordiates: int, vertical_line: int):
        """
        Add an internal vertical wall to the maze.
        """
        self._vertical_walls.add((y_cordiates, vertical_line))

    def get_walls(
        self, x_cordinate: int, y_cordinate: int
    ) -> Tuple[bool, bool, bool, bool]:
        """
        Determine which walls surround a given cell.

        Returns wall presence in the order (north, east, south, west).
        """
        x = x_cordinate
        y = y_cordinate

        north = y == self._height - 1
        south = y == 0
        west = x == 0
        east = x == self._width - 1

        # Internal horizontal walls
        if (x, y + 1) in self._horizontal_walls:
            north = True
        if (x, y) in self._horizontal_walls:
            south = True

        # Internal vertical walls
        if (y, x + 1) in self._vertical_walls:
            east = True
        if (y, x) in self._vertical_walls:
            west = True

        return north, east, south, west

    def sense_walls(self, runner):
        """
        Sense walls relative to the runner's orientation.

        Returns wall information on the left, front, and right.
        """
        x = runner["x"]
        y = runner["y"]
        orient = runner["orientation"]

        walls = self.get_walls(x, y)

        side_map = {
            "N": (3, 0, 1),
            "E": (0, 1, 2),
            "S": (1, 2, 3),
            "W": (2, 3, 0),
        }

        left_i, front_i, right_i = side_map[orient]
        return walls[left_i], walls[front_i], walls[right_i]

    def go_straight(self, runner):
        """
        Move the runner forward by one cell if no wall blocks the path.
        """
        _, front, _ = self.sense_walls(runner)

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
        Turn the runner left or right without changing its position.
        """
        orientations = ["N", "E", "S", "W"]
        idx = orientations.index(runner["orientation"])

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
        Move the runner using a left-hand rule strategy.
        """
        left_wall, front_wall, right_wall = self.sense_walls(runner)

        if not left_wall:
            turned = self._turn(runner, "Left")
            return self.go_straight(turned), "LF"

        if not front_wall:
            return self.go_straight(runner), "F"

        if not right_wall:
            turned = self._turn(runner, "Right")
            return self.go_straight(turned), "RF"

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

        return {"x": x, "y": y, "orientation": opposite}, "B"

    def explore(self, runner, goal=None):
        """
        Explore the maze until the goal is reached.

        Uses local movement decisions rather than global planning.
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
        Return neighbouring cells that can be reached without crossing walls.
        """
        neighbours: List[Tuple[int, int]] = []

        north, east, south, west = self.get_walls(x, y)

        if not north:
            neighbours.append((x, y + 1))
        if not east:
            neighbours.append((x + 1, y))
        if not south:
            neighbours.append((x, y - 1))
        if not west:
            neighbours.append((x - 1, y))

        return neighbours

    def shortest_path(
        self,
        starting: Optional[Tuple[int, int]] = None,
        goal: Optional[Tuple[int, int]] = None,
    ) -> List[Tuple[int, int]]:
        """
        Compute the shortest path using the A* search algorithm.

        This implementation of A* combines the exact path cost from the
        start (g-cost) with a Manhattan-distance heuristic (h-cost) to
        guide the search efficiently toward the goal.
        """
        start = starting if starting is not None else (0, 0)
        target = goal if goal is not None else (self.width - 1, self.height - 1)

        # Manhattan distance heuristic (admissible for grid movement)
        def h(a: tuple[int, int], b: tuple[int, int]) -> int:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        import heapq

        # Priority queue storing (f_cost, node)
        open_set: list[tuple[int, tuple[int, int]]] = []
        heapq.heappush(open_set, (0, start))

        # Cost from start to each node
        g_cost: dict[tuple[int, int], int] = {start: 0}

        # Parent map used to reconstruct the final path
        parent: dict[tuple[int, int], tuple[int, int]] = {}

        # Main A* search loop
        while open_set:
            _, current = heapq.heappop(open_set)

            if current == target:
                break

            cx, cy = current
            for nx, ny in self._get_neighbours(cx, cy):
                neighbour = (nx, ny)
                tentative_g = g_cost[current] + 1

                if neighbour not in g_cost or tentative_g < g_cost[neighbour]:
                    g_cost[neighbour] = tentative_g
                    parent[neighbour] = current
                    f_cost = tentative_g + h(neighbour, target)
                    heapq.heappush(open_set, (f_cost, neighbour))

        if target not in g_cost:
            return []

        # Reconstruct path from goal back to start
        path: list[tuple[int, int]] = []
        node = target

        while node != start:
            path.append(node)
            node = parent[node]

        path.append(start)
        path.reverse()
        return path
