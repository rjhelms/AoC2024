from time import perf_counter

IN_FILE = "04/input.txt"

TARGET_STRING = "MAS"
LETTER_LOCATIONS = {}


def find_at_location(start, direction):
    location = start
    for char in TARGET_STRING:
        if location not in LETTER_LOCATIONS[char]:
            # print(char, location, "miss")
            return False
        # print(char, location, "hit")
        location = [location[0] + direction[0], location[1] + direction[1]]
    return True


def evaluate_pair(candidate_pair):
    x_offset = int(((candidate_pair[0][0] - candidate_pair[1][0]) / 2))
    y_offset = int(((candidate_pair[0][1] - candidate_pair[1][1]) / 2))

    # for each pair, two possible directions to check because string can be forwards or reverse
    # both can be matches

    matches = 0
    if x_offset != 0:
        # print(candidate_pair, x_offset, y_offset)
        if (find_at_location(candidate_pair[0], [-x_offset, 1])) and (
            find_at_location(candidate_pair[1], [x_offset, 1])
        ):
            matches += 1

        if (find_at_location(candidate_pair[0], [-x_offset, -1])) and (
            find_at_location(candidate_pair[1], [x_offset, -1])
        ):
            matches += 1

    else:
        # print(candidate_pair, x_offset, y_offset)
        if (find_at_location(candidate_pair[0], [1, -y_offset])) and (
            find_at_location(candidate_pair[1], [1, y_offset])
        ):
            matches += 1

        if (find_at_location(candidate_pair[0], [-1, -y_offset])) and (
            find_at_location(candidate_pair[1], [-1, y_offset])
        ):
            matches += 1

    return matches


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0

    for char in TARGET_STRING:
        LETTER_LOCATIONS[char] = []

    with open(IN_FILE) as f:
        rows = f.readlines()
        for y in range(len(rows)):
            for x in range(len(rows[y].strip())):
                if rows[y][x] in TARGET_STRING:
                    LETTER_LOCATIONS[rows[y][x]].append([x, y])

    # print(LETTER_LOCATIONS)
    candidate_pairs = []
    candidate_starts = LETTER_LOCATIONS[TARGET_STRING[0]].copy()
    while len(candidate_starts) > 0:
        start_location = candidate_starts.pop()
        for check_offset in [[2, 0], [-2, 0], [0, 2], [0, -2]]:
            pair_location = [
                start_location[0] + check_offset[0],
                start_location[1] + check_offset[1],
            ]
            if pair_location in candidate_starts:
                candidate_pairs.append([start_location, pair_location])

    for pair in candidate_pairs:
        score += evaluate_pair(pair)

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
