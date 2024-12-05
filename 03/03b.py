from time import perf_counter
import re

IN_FILE = "03/input.txt"

if __name__ == "__main__":
    start_time = perf_counter()

    pairs = []
    score = 0

    with open(IN_FILE) as f:
        instructions = re.findall(r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))", f.read())

    active = True
    for line in instructions:
        if len(line[1]) > 0:
            active = True
        elif len(line[2]) > 0:
            active = False
        elif active == True:
            pair = [int(val) for val in line[0][4:-1].split(",")]
            score += pair[0] * pair[1]

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
