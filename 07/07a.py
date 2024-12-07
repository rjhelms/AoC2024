from time import perf_counter

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
        for i in range(2 ** (len(CALIBRATIONS[cal]) - 1)):
            result = CALIBRATIONS[cal][0]
            for j in range(1, len(CALIBRATIONS[cal])):
                if i & 1:
                    result += CALIBRATIONS[cal][j]
                else:
                    result *= CALIBRATIONS[cal][j]
                i >>= 1
            if result == cal:
                score += cal
                break

    print(score)

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
