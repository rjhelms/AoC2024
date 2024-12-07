from time import perf_counter

IN_FILE = "06/input.txt"

# starting with up, in clockwise order
MOVEMENT_VECTORS = [[0, -1], [1, 0], [0, 1], [-1, 0]]
X_SIZE = 0
Y_SIZE = 0

GUARD_POSITION = [0, 0]
GUARD_DIRECTION = 0
WALL_LOCATIONS = []
VISITED_LOCATIONS = []

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        rows = f.readlines()
        X_SIZE = len(rows[0].strip())
        Y_SIZE = len(rows)
        for x in range(X_SIZE):
            for y in range(Y_SIZE):
                if rows[y][x] == "#":
                    WALL_LOCATIONS.append([x, y])
                elif rows[y][x] == "^":
                    GUARD_POSITION = [x, y]

    while (
        GUARD_POSITION[0] >= 0
        and GUARD_POSITION[0] < X_SIZE
        and GUARD_POSITION[1] >= 0
        and GUARD_POSITION[1] < Y_SIZE
    ):
        candidate_location = [
            GUARD_POSITION[0] + MOVEMENT_VECTORS[GUARD_DIRECTION][0],
            GUARD_POSITION[1] + MOVEMENT_VECTORS[GUARD_DIRECTION][1],
        ]
        if candidate_location in WALL_LOCATIONS:
            GUARD_DIRECTION += 1
            GUARD_DIRECTION %= 4
        else:
            if GUARD_POSITION not in VISITED_LOCATIONS:
                VISITED_LOCATIONS.append(GUARD_POSITION)
            GUARD_POSITION = candidate_location

    print(len(VISITED_LOCATIONS))
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
