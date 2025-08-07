# Read the puzzle
with open("puzzle.txt", "r") as file:
    puzzle = file.read()

puzzle = puzzle.splitlines()

expansion_rate = 1000000 # Change according to the part challenge.

# Double empty columns and rows
# How?
# Recording the position of each galaxy in a dictionary
# We eliminate columns and rows as we record galaxy positions.

# Track the column indexes.

columns_to_double = list(range(len(puzzle[0])))

rows_to_double = []

galaxies_positions = {}

galaxy_number = 1

for row_index, row in enumerate(puzzle):
    if '#' not in row:
        rows_to_double.append(row_index)
    for col_index, col in enumerate(row):
        if '#' in col:
            if col_index in columns_to_double:
                columns_to_double.remove(col_index)
            galaxies_positions[galaxy_number] = [row_index, col_index]
            galaxy_number += 1

# print(f"Columns to double: {columns_to_double}")
# print(f"Rows to double: {rows_to_double}")
# print(f"Galaxies positions: {galaxies_positions}")

# Double the cols and rows
for galaxy in galaxies_positions:
    galaxy_row = galaxies_positions[galaxy][0]
    galaxy_col = galaxies_positions[galaxy][1]
    for row in rows_to_double:
        if galaxy_row > row:
            galaxies_positions[galaxy][0] += (expansion_rate - 1)
    for col in columns_to_double:
        if galaxy_col > col:
            galaxies_positions[galaxy][1] += (expansion_rate - 1)

# print(f"Galaxies postions after expansion: {galaxies_positions}")

total_path_lengths = 0
remaining_pairs = list(galaxies_positions.keys())
for galaxy_one in galaxies_positions:
    remaining_pairs.remove(galaxy_one)
    # print("=================================")
    # print("Remaining pairs: ", remaining_pairs)
    # print("=================================")
    for galaxy_two in remaining_pairs:
        galaxy_one_row = galaxies_positions[galaxy_one][0]
        galaxy_one_col = galaxies_positions[galaxy_one][1]

        galaxy_two_row = galaxies_positions[galaxy_two][0]
        galaxy_two_col = galaxies_positions[galaxy_two][1]

        row_diff = abs(galaxy_two_row - galaxy_one_row)
        col_diff = abs(galaxy_two_col - galaxy_one_col)

        shortest_path = row_diff + col_diff
        # print(f"Shortest path length from galaxy{galaxy_one} to galaxy {galaxy_two} is {shortest_path}")
        
        total_path_lengths += shortest_path

print(f"Total sum of the lengths: {total_path_lengths}")
