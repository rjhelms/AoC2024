from time import perf_counter
from collections import defaultdict

IN_FILE = "10/input.txt"

TERRAIN = defaultdict(lambda: -1)


def search(start_tile):
    closed_list = []
    open_list = [start_tile]
    score = 0

    while len(open_list) > 0:
        current = open_list.pop()
        closed_list.append(current)
        target = TERRAIN[current] + 1
        candidates = [
            (current[0] - 1, current[1]),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0], current[1] + 1),
        ]
        for tile in candidates:
            if tile not in closed_list and TERRAIN[tile] == target:
                if target == 9:
                    score += 1
                open_list.append(tile)
    return score


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0
    start_tiles = []
    with open(IN_FILE) as f:
        lines = f.readlines()
        for y in range(len(lines)):
            for x in range(len(lines[y].strip())):
                val = int(lines[y][x])
                TERRAIN[(x, y)] = val
                if val == 0:
                    start_tiles.append((x, y))

    for tile in start_tiles:
        score += search(tile)

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
