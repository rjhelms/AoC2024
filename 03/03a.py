from time import perf_counter
import re

IN_FILE = "03/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    pairs = []
    score = 0

    with open(IN_FILE) as f:
        pairs = [
            [int(y) for y in x[4:-1].split(",")]
            for x in re.findall(r"mul\(\d+,\d+\)", f.read())
        ]

    for pair in pairs:
        score += pair[0] * pair[1]

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
