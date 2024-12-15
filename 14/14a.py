from time import perf_counter

IN_FILE = "14/input.txt"

WORLD_X = 101
WORLD_Y = 103

ITERATIONS = 100

if __name__ == "__main__":
    start_time = perf_counter()

    robot_positions = []

    with open(IN_FILE) as f:
        for line in f:
            start_pos = [int(x) for x in line.split(" ")[0].split("=")[1].split(",")]
            move_vector = [int(x) for x in line.split(" ")[1].split("=")[1].split(",")]

            # no need to iterate - can just add up all 100 movements and modulo
            end_pos = [
                (start_pos[0] + move_vector[0] * ITERATIONS) % WORLD_X,
                (start_pos[1] + move_vector[1] * ITERATIONS) % WORLD_Y,
            ]
            robot_positions.append(end_pos)

    x_divider = (WORLD_X - 1) / 2
    y_divider = (WORLD_Y - 1) / 2

    quadrant_counts = [0, 0, 0, 0]
    for robot in robot_positions:
        robot_quadrant = 0
        if robot[0] == x_divider or robot[1] == y_divider:
            continue
        if robot[0] > x_divider:
            robot_quadrant += 1
        if robot[1] > y_divider:
            robot_quadrant += 2
        quadrant_counts[robot_quadrant] += 1

    score = 1
    for quad in quadrant_counts:
        score *= quad

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
