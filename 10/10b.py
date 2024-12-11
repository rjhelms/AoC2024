from time import perf_counter
from collections import defaultdict

IN_FILE = "10/input.txt"

TERRAIN = defaultdict(lambda: -1)


def search(start_tile, closed_list=[]):
    if TERRAIN[start_tile] == 9:
        return 1
    score = 0
    target = TERRAIN[start_tile] + 1
    closed_list.append(start_tile)
    candidates = [
        (start_tile[0] - 1, start_tile[1]),
        (start_tile[0] + 1, start_tile[1]),
        (start_tile[0], start_tile[1] - 1),
        (start_tile[0], start_tile[1] + 1),
    ]
    for tile in candidates:
        if tile not in closed_list and TERRAIN[tile] == target:
            score += search(tile, closed_list=closed_list.copy())
    return score


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0
    start_tiles = []
    with open(IN_FILE) as f:
        lines = f.readlines()
        for y in range(len(lines)):
            for x in range(len(lines[y].strip())):
                if lines[y][x] != ".":
                    val = int(lines[y][x])
                    TERRAIN[(x, y)] = val
                    if val == 0:
                        start_tiles.append((x, y))

    for tile in start_tiles:
        score += search(tile)

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
