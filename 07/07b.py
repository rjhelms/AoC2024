from time import perf_counter
from itertools import product

IN_FILE = "07/input.txt"

CALIBRATIONS = {}

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        for line in f:
            line = line.split(":")
            CALIBRATIONS[int(line[0])] = [int(x) for x in line[1].split()]

    score = 0

    for cal in CALIBRATIONS:
        for i in product(range(3), repeat=(len(CALIBRATIONS[cal]) - 1)):
            result = CALIBRATIONS[cal][0]
            for j in range(len(CALIBRATIONS[cal]) - 1):
                if i[j] == 0:
                    result += CALIBRATIONS[cal][j + 1]
                elif i[j] == 1:
                    result *= CALIBRATIONS[cal][j + 1]
                elif i[j] == 2:
                    result = int(str(result) + str(CALIBRATIONS[cal][j + 1]))

                # since all operations increase result, escape if it's already exceeded the target
                if result > cal:
                    break

            if result == cal:
                score += cal
                break

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
