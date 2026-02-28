def create_runner(x: int = 0, y: int = 0, orientation: str = "N"):
    """
    Create and returns a runner represented as a dict,
    default position will be (0, 0) facing north.
    """
    return {"x": x, "y": y, "orientation": orientation}


def get_x(runner):
    """
    Returns the x coordinate of the runner.
    """
    return runner["x"]


def get_y(runner):
    """
    Returns the y coordinate of the runner.
    """
    return runner["y"]


def get_orientation(runner):
    """
    Returns the facing direction of the runner
    """
    return runner["orientation"]


def turn(runner, direction: str):
    """
    Turns the runner left or right.
    The position stays the same, only orientation changes.
    """
    orientations = ["N", "E", "S", "W"]

    current = runner["orientation"]
    idx = orientations.index(current)

    if direction == "Left":
        new_orientation = orientations[(idx - 1) % 4]
    elif direction == "Right":
        new_orientation = orientations[(idx + 1) % 4]
    else:
        new_orientation = current

    return {"x": runner["x"], "y": runner["y"], "orientation": new_orientation}


def forward(runner):
    """Moves the runner forward by 1 cell.
    # The orientation stays the same; only x/y change."""

    x = runner["x"]
    y = runner["y"]
    orientation = runner["orientation"]

    deltas = {"N": (0, 1), "E": (1, 0), "S": (0, -1), "W": (-1, 0)}
    dx, dy = deltas[orientation]

    return {"x": x + dx, "y": y + dy, "orientation": orientation}
