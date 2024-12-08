from time import perf_counter
from collections import defaultdict
from itertools import combinations

IN_FILE = "08/input.txt"

X_SIZE = 0
Y_SIZE = 0

ANTENNA_LOCATIONS = defaultdict(list)
ANTINODES = []


def valid_position(position):
    return (
        position[0] >= 0
        and position[0] < X_SIZE
        and position[1] >= 0
        and position[1] < Y_SIZE
    )


if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        rows = f.readlines()
        X_SIZE = len(rows[0].strip())
        Y_SIZE = len(rows)
        for x in range(X_SIZE):
            for y in range(Y_SIZE):
                if rows[y][x] != ".":
                    ANTENNA_LOCATIONS[rows[y][x]].append((x, y))

    for type in ANTENNA_LOCATIONS:
        for i in combinations(ANTENNA_LOCATIONS[type], 2):
            offset = (i[0][0] - i[1][0], i[0][1] - i[1][1])

            for walk in i:
                while valid_position(walk):
                    if walk not in ANTINODES:
                        ANTINODES.append(walk)
                    walk = (walk[0] + offset[0], walk[1] + offset[1])
                # flip offset for next walk
                offset = (-offset[0], -offset[1])

    print(len(ANTINODES))
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
