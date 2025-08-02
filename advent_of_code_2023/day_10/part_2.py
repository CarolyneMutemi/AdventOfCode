from part_1 import find_starting_point

# 1. Get the tiles in the loop in a per line structure.
# Read the puzzle input.
with open("puzzle.txt", "r") as file:
    puzzle_input = file.read().splitlines()

# Keep track of the lines and tiles within the loop
loop_tiles_indexes = {}

def track_loop(line_index: int, tile_index: int):
    if line_index in loop_tiles_indexes:
        loop_tiles_indexes[line_index].append(tile_index)
    else:
        loop_tiles_indexes[line_index] = [tile_index]

# Find the starting point in the puzzle input.
starting_point_line_index, starting_point_tile_index = find_starting_point(puzzle_input)

# Track the starting point.
track_loop(starting_point_line_index, starting_point_tile_index)

right_connectors = {
    '7': 'bottom',
    'J': 'top',
    '-': 'right'
    }
left_connectors = {
    'F': 'bottom',
    'L': 'top',
    '-': 'left'
    }
bottom_connectors = {
    'J': 'left',
    'L': 'right',
    '|': 'bottom'
    }
top_connectors = {
    'F': 'right',
    '7': 'left',
    '|': 'top'}

# Find the next tile after S i.e starting point.
def find_s_connecting_tile(s_line_index: int, s_tile_index: int) -> tuple:
    """
    Find the next tile connecting the starting tile.
    Basically we check a tile around S that is correctly positioned - this is what's unique about the S tile.
    The other tiles can have correctly positioned tiles around them and not be the connecting tile apart from S tile.

    Return:
        (next_line_index, next_tile_index, direction_headed) - a tuple.
    """
    top_tile = puzzle_input[s_line_index - 1][s_tile_index] if s_line_index > 0 else None
    right_tile = puzzle_input[s_line_index][s_tile_index + 1] if (s_tile_index + 1) < len(puzzle_input[s_line_index]) else None
    bottom_tile = puzzle_input[s_line_index + 1][s_tile_index] if (s_line_index + 1) < len(puzzle_input) else None
    left_tile = puzzle_input[s_line_index][s_tile_index - 1] if s_tile_index > 0 else None

    if top_tile in top_connectors:
        return (s_line_index - 1, s_tile_index, top_connectors[top_tile])
    if right_tile in right_connectors:
        return (s_line_index, s_tile_index + 1, right_connectors[right_tile])
    if bottom_tile in bottom_connectors:
        return (s_line_index + 1, s_tile_index, bottom_connectors[bottom_tile])
    if left_tile in left_connectors:
        return (s_line_index, s_tile_index - 1, left_connectors[left_tile])

current_line_index, current_tile_index, direction_headed = find_s_connecting_tile(starting_point_line_index, starting_point_tile_index)
track_loop(current_line_index, current_tile_index)

# Get the tiles in the loop
while True:
    if direction_headed == 'bottom':
        current_line_index += 1
        current_tile = puzzle_input[current_line_index][current_tile_index]
        direction_headed = bottom_connectors.get(current_tile, None)
    elif direction_headed == 'left':
        current_tile_index -= 1
        current_tile = puzzle_input[current_line_index][current_tile_index]
        direction_headed = left_connectors.get(current_tile, None)
    elif direction_headed == 'top':
        current_line_index -= 1
        current_tile = puzzle_input[current_line_index][current_tile_index]
        direction_headed = top_connectors.get(current_tile, None)
    else:
        current_tile_index += 1
        current_tile = puzzle_input[current_line_index][current_tile_index]
        direction_headed = right_connectors.get(current_tile, None)
    if current_tile == 'S' or not direction_headed:
        break
    track_loop(current_line_index, current_tile_index)

# Sort the loop.
for line in loop_tiles_indexes:
    loop_tiles_indexes[line].sort()


# Start the inner loop check.
# If F is connected to J then the inner side remains same - same thing with L and 7.
# Otherwise if F is connected to 7  the inner side changes - same thing with L and J.
# The other patterns, ignoring -, will interchange their inner side given that they don't connect horizontally.

def get_inner_side(previous_inner_side, previous_tile, current_tile):
    """
    Get the current inner side of the loop from the current tiles perspective.
    """
    if (previous_tile == 'F' and current_tile == 'J') or (previous_tile == 'L' and current_tile == '7') or current_tile == '-':
        return previous_inner_side
    return 'left' if previous_inner_side == 'right' else 'right'

inner_tiles_count = 0

for line_index, tile_indexes in loop_tiles_indexes.items():
    current_tile = puzzle_input[line_index][tile_indexes[0]]
    if current_tile not in ['F', 'L', '|']:
        raise ValueError(f"Some odd tile is at the start: {current_tile}.")
    previous_inner_side = None
    previous_tile = None

    for index, tile_index in enumerate(tile_indexes):
        tile = puzzle_input[line_index][tile_index]
        if tile != '-': # Ignore the '-' tiles because they don't determine the inner side of the loop, they just connect determining tiles.
            current_inner_side = get_inner_side(previous_inner_side, previous_tile, tile) if index > 0 else 'right' # First inner side is right
            if previous_inner_side == 'right' and current_inner_side == 'left':
                diff = tile_indexes[index] - tile_indexes[index - 1] - 1
                inner_tiles_count += diff
            previous_inner_side = current_inner_side
            previous_tile = tile

print("Inner tiles count: ", inner_tiles_count)
