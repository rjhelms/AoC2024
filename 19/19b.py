from time import perf_counter
from functools import cache

IN_FILE = "19/input.txt"

PATTERNS = []


@cache
def validate_string(string):
    score = 0
    for pattern in PATTERNS:
        if pattern == string:
            score += 1
        elif pattern == string[: len(pattern)]:
            score += validate_string(string[len(pattern) :])
    return score


if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        lines = f.readlines()
        PATTERNS = [x.strip() for x in lines[0].split(",")]
        designs = [x.strip() for x in lines[2:]]
    # print(patterns)
    # print(designs)

    score = 0
    for design in designs:
        score += validate_string(design)

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
