from time import perf_counter
from collections import defaultdict

IN_FILE = "15/input.txt"

MAP = defaultdict(lambda: ".")

MOVE_VECTORS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}

if __name__ == "__main__":
    start_time = perf_counter()
    world_x = 0
    world_y = 0

    robot_coord = (None, None)
    instructions = ""
    with open(IN_FILE) as f:
        got_map = False
        y = 0
        for line in f:
            if len(line) == 1:
                got_map = True
            else:
                if got_map:
                    instructions += line.strip()
                else:
                    for x in range(len(line.strip())):
                        MAP[(x, y)] = line[x]
                        if line[x] == "@":
                            robot_coord = (x, y)
                    y += 1
                    world_y = y
                    world_x = len(line.strip())

    for char in instructions:

        # determine if move is possible by walking forward
        move_blocked = False
        next_step = robot_coord
        while not move_blocked:
            next_step = (
                next_step[0] + MOVE_VECTORS[char][0],
                next_step[1] + MOVE_VECTORS[char][1],
            )
            if MAP[next_step] == ".":
                # if hit an empty space, move is possible - end walk
                break
            elif MAP[next_step] == "#":
                move_blocked = True

        if not move_blocked:
            push_done = False

            # step backwards along the walk, copying each tile forward
            while not push_done:
                back_step = (
                    next_step[0] - MOVE_VECTORS[char][0],
                    next_step[1] - MOVE_VECTORS[char][1],
                )
                MAP[next_step] = MAP[back_step]

                # and then put an empty tile where the robot was
                if back_step == robot_coord:
                    MAP[back_step] = "."
                    robot_coord = next_step
                    push_done = True
                next_step = back_step

    score = 0
    for y in range(world_y):
        for x in range(world_x):
            if MAP[(x, y)] == "O":
                score += x + 100 * y

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
