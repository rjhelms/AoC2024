from time import perf_counter

IN_FILE = "04/input.txt"

TARGET_STRING = "XMAS"
LETTER_LOCATIONS = {}


def find_at_location(start, direction):
    location = start
    for char in TARGET_STRING:
        if location not in LETTER_LOCATIONS[char]:
            return False
        location = [location[0] + direction[0], location[1] + direction[1]]
    return True


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0

    for char in TARGET_STRING:
        LETTER_LOCATIONS[char] = []

    with open(IN_FILE) as f:
        rows = f.readlines()
        for y in range(len(rows)):
            for x in range(len(rows[y].strip())):
                LETTER_LOCATIONS[rows[y][x]].append([x, y])

    for candidate in LETTER_LOCATIONS[TARGET_STRING[0]]:
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x != 0 or y != 0:
                    if find_at_location(candidate, [x, y]):
                        score += 1

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
