"""The warehouse map and small helper functions for working with it.

A cell is written as (row, col). Row 0 is the top line of the map,
col 0 is the left-most character.
"""

# Map symbols
FLOOR = "."
SHELF = "#"
PACKING = "P"
CHARGER = "C"

# The default warehouse. Each string is one row.
# Shelves are in blocks with aisles between them, like a real warehouse.
WAREHOUSE_MAP = [
    "C.............",
    "..##..##..##..",
    "..##..##..##..",
    "..##..##..##..",
    "..............",
    "..##..##..##..",
    "..##..##..##..",
    "..##..##..##..",
    ".............P",
]

# The four directions a robot can move: up, down, left, right.
# Each is a (row change, col change) pair. No diagonal moves.
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def load_grid(rows=WAREHOUSE_MAP):
    """Turn a list of strings into a grid (a list of lists of characters).

    Raises ValueError if the rows are not all the same length.
    """
    if not rows:
        raise ValueError("map is empty")
    width = len(rows[0])
    for row in rows:
        if len(row) != width:
            raise ValueError("all map rows must be the same length")
    # list(row) splits "C.#" into ["C", ".", "#"], so each cell can be read with grid[r][c]
    return [list(row) for row in rows]


def in_bounds(grid, cell):
    """True if the cell is inside the map."""
    row, col = cell
    return 0 <= row < len(grid) and 0 <= col < len(grid[0])


def is_walkable(grid, cell):
    """True if a robot can stand on this cell (inside the map and not a shelf)."""
    if not in_bounds(grid, cell):
        return False
    row, col = cell
    return grid[row][col] != SHELF


def neighbors(grid, cell):
    """Return the walkable cells directly up, down, left and right of this cell."""
    row, col = cell
    result = []
    for d_row, d_col in DIRECTIONS:
        next_cell = (row + d_row, col + d_col)
        if is_walkable(grid, next_cell):
            result.append(next_cell)
    return result


def find(grid, symbol):
    """Return the (row, col) of the first cell with this symbol, or None if it isn't on the map."""
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value == symbol:
                return (row_index, col_index)
    return None
