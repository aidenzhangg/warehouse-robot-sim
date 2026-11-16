"""A* pathfinding on the warehouse grid.

A* finds the shortest path by always exploring the cell that looks most promising:
the one with the smallest  f = g + h
    g = steps already taken from the start to this cell (known exactly)
    h = estimated steps left from this cell to the goal (a guess, see manhattan)
"""

import heapq

from sim.grid import is_walkable, neighbors


def manhattan(a, b):
    """Estimated steps between two cells if there were no shelves in the way.

    With only up/down/left/right moves you can never do better than this,
    so A* is guaranteed to find the shortest path.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, goal):
    """Walk backwards from the goal using came_from, then flip the list to start -> goal."""
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = came_from[cell]
    path.reverse()
    return path


def astar(grid, start, goal):
    """Return the shortest path from start to goal as a list of (row, col) cells.

    The list includes both start and goal. Returns None if there is no path.
    """
    if not is_walkable(grid, start) or not is_walkable(grid, goal):
        return None

    # The "open set": cells we've discovered but not explored yet.
    # heapq keeps the smallest tuple at the front, so we always pop the lowest f.
    # Tuple = (f, h, cell). If two cells tie on f, the one with smaller h
    # (closer to the goal) wins the tie.
    open_heap = [(manhattan(start, goal), manhattan(start, goal), start)]

    came_from = {start: None}  # cell -> the cell we stepped from to reach it
    g_cost = {start: 0}        # cell -> fewest steps found so far from start

    while open_heap:
        _, _, current = heapq.heappop(open_heap)

        if current == goal:
            return reconstruct_path(came_from, goal)

        for next_cell in neighbors(grid, current):
            new_g = g_cost[current] + 1  # every move costs 1 step

            # Only keep this route if it's the first or the shortest way to next_cell so far
            if next_cell not in g_cost or new_g < g_cost[next_cell]:
                g_cost[next_cell] = new_g
                came_from[next_cell] = current
                h = manhattan(next_cell, goal)
                heapq.heappush(open_heap, (new_g + h, h, next_cell))

    # Ran out of cells to explore without reaching the goal
    return None
