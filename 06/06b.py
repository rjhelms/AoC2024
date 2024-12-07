from time import perf_counter
from collections import defaultdict

IN_FILE = "06/input.txt"

# starting with up, in clockwise order
MOVEMENT_VECTORS = [[0, -1], [1, 0], [0, 1], [-1, 0]]

X_SIZE = 0
Y_SIZE = 0

GUARD_POSITION = (0, 0)
GUARD_DIRECTION = 0
WALL_LOCATIONS = []

# for each visited location, store the direction facing when it was entered
VISITED_LOCATIONS = defaultdict(list)


def valid_position(position):
    return (
        position[0] >= 0
        and position[0] < X_SIZE
        and position[1] >= 0
        and position[1] < Y_SIZE
    )


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0

    with open(IN_FILE) as f:
        rows = f.readlines()
        X_SIZE = len(rows[0].strip())
        Y_SIZE = len(rows)
        for x in range(X_SIZE):
            for y in range(Y_SIZE):
                if rows[y][x] == "#":
                    WALL_LOCATIONS.append((x, y))
                elif rows[y][x] == "^":
                    GUARD_POSITION = (x, y)

    start_position = GUARD_POSITION

    # do simple walk through path (from part 1) to build list of potential wall locations
    potential_wall_locations = []
    while valid_position(GUARD_POSITION):
        candidate_location = (
            GUARD_POSITION[0] + MOVEMENT_VECTORS[GUARD_DIRECTION][0],
            GUARD_POSITION[1] + MOVEMENT_VECTORS[GUARD_DIRECTION][1],
        )
        if candidate_location in WALL_LOCATIONS:
            GUARD_DIRECTION += 1
            GUARD_DIRECTION %= 4
        else:
            if GUARD_POSITION not in potential_wall_locations:
                potential_wall_locations.append(GUARD_POSITION)
            GUARD_POSITION = candidate_location

    print(len(potential_wall_locations))
    iter = 0

    # brute force because I'm not clever
    # rather than checking every location, only places that unmodified path travels through
    for loc in potential_wall_locations:
        iter += 1
        if iter % 10 == 0:
            print(".", end="", flush=True)
        if iter % 500 == 0:
            print("", score, "(", iter, "/", len(potential_wall_locations), ")")

        if loc != start_position and loc not in WALL_LOCATIONS:
            # add this location to local list of wall locations
            iter_wall_locations = WALL_LOCATIONS.copy()
            iter_wall_locations.append(loc)
            done_iter = False

            # reset path
            GUARD_DIRECTION = 0
            GUARD_POSITION = start_position
            VISITED_LOCATIONS = defaultdict(list)
            while not done_iter:
                if not valid_position(GUARD_POSITION):
                    # print(x, y, " escaped")
                    done_iter = True
                else:
                    candidate_location = (
                        GUARD_POSITION[0] + MOVEMENT_VECTORS[GUARD_DIRECTION][0],
                        GUARD_POSITION[1] + MOVEMENT_VECTORS[GUARD_DIRECTION][1],
                    )
                    if candidate_location in iter_wall_locations:
                        GUARD_DIRECTION += 1
                        GUARD_DIRECTION %= 4
                    elif GUARD_DIRECTION in VISITED_LOCATIONS[GUARD_POSITION]:
                        # print(x, y, " caught in loop")
                        score += 1
                        done_iter = True
                    else:
                        VISITED_LOCATIONS[GUARD_POSITION].append(GUARD_DIRECTION)
                        GUARD_POSITION = candidate_location

    print()
    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
