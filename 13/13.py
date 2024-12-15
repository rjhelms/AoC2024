from time import perf_counter
import numpy as np

IN_FILE = "13/input.txt"

# some results returned by numpy are not quite integers
# so accept a certain fudge factor
ROUND_CHECK = 0.0001  # this value is arbitrary but gets the right result ¯\_(ツ)_/¯

# set to 0 for part A and 10000000000000 for part B
OFFSET = 10000000000000

if __name__ == "__main__":
    start_time = perf_counter()
    score = 0
    with open(IN_FILE) as f:
        row = 0
        for line in f:
            if row == 0:
                coefficients = []
            if row < 2:
                coefficients.append(
                    [int(x.split("+")[1]) for x in line.split(":")[1].split(",")]
                )
                row += 1
            elif row == 2:
                # need to swizzle coefficients:
                # first row is the effect of each button on X coord,
                # second row is effect of each button on Y coord
                A = np.array(
                    [
                        [coefficients[0][0], coefficients[1][0]],
                        [coefficients[0][1], coefficients[1][1]],
                    ]
                )

                B = np.array(
                    [
                        int(x.split("=")[1]) + OFFSET
                        for x in line.split(":")[1].split(",")
                    ]
                )

                C = np.linalg.solve(A, B)

                if (
                    abs(round(C[0]) - C[0]) < ROUND_CHECK
                    and abs(round(C[1]) - C[1]) < ROUND_CHECK
                ):
                    score += round(C[0]) * 3 + round(C[1])
                row += 1
            elif row == 3:
                row = 0

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
