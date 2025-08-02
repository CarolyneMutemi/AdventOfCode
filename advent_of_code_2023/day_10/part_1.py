# Read the puzzle input.
with open("puzzle.txt", "r") as file:
    puzzle_input = file.readlines()

def find_starting_point(puzzle_input):
    """
    Finds the starting point 'S' in the puzzle input.
    Returns:
        - The line index of the starting point.
        - The tile index of the starting point.
    """
    for index, line in enumerate(puzzle_input):
        if "S" in line:
            return index, line.index("S")
    return None, None

# Find the starting point in the puzzle input.
starting_point_line_index, starting_point_tile_index = find_starting_point(puzzle_input)

# print("Starting point line index", starting_point_line_index)
# print("Starting point tile index", starting_point_tile_index)

current_line_index = starting_point_line_index
current_tile_index = starting_point_tile_index
current_tile = puzzle_input[current_line_index][current_tile_index]



def find_next_tile(current_tile, current_line_index, current_tile_index, direction_from):
    """
    Finds the next connected tile.
    Returns:
        - The next tile character.
        - The line index of the next tile.
        - The tile index of the next tile.
        - The direction from which the next tile is approached.
    """

    # Define the expected connections for the four directions of a tile.
    expected_connection = {
        "above": ["|", "7", "F"],
        "right": ["-", "J", "7"],
        "below": ["|", "L", "J"],
        "left": ["-", "L", "F"]
    }

    # Find the tiles above, right, below, and left of the current tile.
    above_tile = puzzle_input[(current_line_index - 1)][current_tile_index] if current_line_index > 0 else None
    right_tile = puzzle_input[current_line_index][current_tile_index + 1] if current_tile_index < len(puzzle_input[current_line_index]) else None
    below_tile = puzzle_input[(current_line_index + 1)][current_tile_index] if current_line_index < len(puzzle_input) else None
    left_tile = puzzle_input[current_line_index][current_tile_index - 1] if current_tile_index > 0 else None

    # Check the connections based on the current tile and the direction from which it was approached to avoid looping over just one connection.
    if current_tile in ["|", "L", "J", "S"] and above_tile in expected_connection["above"] and direction_from != "above":
        return above_tile, current_line_index - 1, current_tile_index, "below"
    if current_tile in ["-", "L", "F", "S"] and right_tile in expected_connection["right"] and direction_from != "right":
        return right_tile, current_line_index, current_tile_index + 1, "left"
    if current_tile in ["|", "7", "F", "S"] and below_tile in expected_connection["below"] and direction_from != "below":
        return below_tile, current_line_index + 1, current_tile_index, "above"
    if current_tile in ["-", "J", "7", "S"] and left_tile in expected_connection["left"] and direction_from != "left":
        return left_tile, current_line_index, current_tile_index - 1, "right"

    # Next tile is either "S" or a tile that has no connections.
    # print(f"Tile '{current_tile}' on line index {current_line_index} at tile index {current_tile_index} is either connected to the starting point or has no connections.")
    return None, None, None, None


tiles = 1 # Keep track of the number of tiles in the loop, starting with the starting tile.

# Start the search for the next tile from the starting point.
current_tile, current_line_index, current_tile_index, direction_from = find_next_tile(current_tile, current_line_index, current_tile_index, "start")
tiles += 1

# Continue finding tiles until no more connected tiles are found or the starting point is reached again.
while True:
    current_tile = puzzle_input[current_line_index][current_tile_index]
    current_tile, current_line_index, current_tile_index, direction_from = find_next_tile(current_tile, current_line_index, current_tile_index, direction_from)
    
    if not current_tile:
        break

    tiles += 1
    

if __name__ == "__main__":
    print("Total tiles in loop:", tiles)
    print("Farthest tile number from starting point:", tiles // 2)
    
