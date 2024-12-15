from time import perf_counter
from collections import defaultdict

IN_FILE = "14/input.txt"

WORLD_X = 101
WORLD_Y = 103

ITERATIONS = 100


class Robot:
    def __init__(self, position, movement):
        self.position = (position[0], position[1])
        self.movement = (movement[0], movement[1])

    def move(self):
        self.position = (
            (self.position[0] + self.movement[0]) % WORLD_X,
            (self.position[1] + self.movement[1]) % WORLD_Y,
        )


if __name__ == "__main__":
    start_time = perf_counter()

    robots = []

    with open(IN_FILE) as f:
        for line in f:
            start_pos = [int(x) for x in line.split(" ")[0].split("=")[1].split(",")]
            move_vector = [int(x) for x in line.split(" ")[1].split("=")[1].split(",")]
            robots.append(Robot(start_pos, move_vector))

    iter = 0

    while True:
        position_dict = defaultdict(lambda: 0)

        # assumption that tree occurs when every robot is in a unique position
        # (this is not stated anywhere but seems to be the case)

        unique_pos = True

        for robot in robots:
            robot.move()
            position_dict[robot.position] += 1
            if position_dict[robot.position] > 1:
                unique_pos = False
        iter += 1

        if unique_pos:
            print()
            for y in range(WORLD_Y):
                for x in range(WORLD_X):
                    here_bot = False
                    for robot in robots:
                        if robot.position == (x, y):
                            here_bot = True
                            break
                    if here_bot:
                        print("#", end="")
                    else:
                        print(" ", end="")
                print()
            print(iter)
            break

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
