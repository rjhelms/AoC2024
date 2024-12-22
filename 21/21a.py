from time import perf_counter

IN_FILE = "21/input.txt"

NUM_PAD_POSITIONS = {
    "0": (1, 3),
    "1": (0, 2),
    "2": (1, 2),
    "3": (2, 2),
    "4": (0, 1),
    "5": (1, 1),
    "6": (2, 1),
    "7": (0, 0),
    "8": (1, 0),
    "9": (2, 0),
    "A": (2, 3),
    None: (0, 3),
}

DIR_PAD_POSITIONS = {
    "^": (1, 0),
    "<": (0, 1),
    "v": (1, 1),
    ">": (2, 1),
    "A": (2, 0),
    None: (0, 0),
}


def get_moves(position: tuple[int], target: str, pad: dict) -> list[str]:
    target_pos = pad[target]
    x_mov = target_pos[0] - position[0]
    y_mov = target_pos[1] - position[1]

    x_str = ""
    y_str = ""
    if x_mov < 0:
        x_str = "<" * -x_mov
    elif x_mov > 0:
        x_str = ">" * x_mov

    if y_mov < 0:
        y_str = "^" * -y_mov
    elif y_mov > 0:
        y_str = "v" * y_mov

    if x_mov == 0 and y_mov == 0:
        return ["A"]
    if x_mov == 0:
        return [y_str + "A"]
    elif y_mov == 0:
        return [x_str + "A"]
    else:
        # ensure no path that goes over an empty spot
        if (position[0] == pad[None][0]) and (target_pos[1] == pad[None][1]):
            return [x_str + y_str + "A"]
        elif (position[1] == pad[None][1]) and (target_pos[0] == pad[None][0]):
            return [y_str + x_str + "A"]

        return [x_str + y_str + "A", y_str + x_str + "A"]


def get_paths(targets: list[str], pad: dict) -> list[str]:
    results = []

    for target in targets:
        position = pad["A"]
        paths = [""]
        for char in target:
            for _ in range(len(paths)):
                path = paths.pop(0)
                paths.extend([path + x for x in get_moves(position, char, pad)])
            position = pad[char]
        results.extend(paths)
    results.sort(key=len)
    return results


if __name__ == "__main__":
    start_time = perf_counter()

    score = 0
    with open(IN_FILE) as f:
        for line in f:
            paths = get_paths([line.strip()], NUM_PAD_POSITIONS)
            for _ in range(2):
                paths = get_paths(paths, DIR_PAD_POSITIONS)
                paths.sort(key=len)
                paths = [x for x in paths if len(x) == len(paths[0])]

            paths.sort(key=len)
            score += len(paths[0]) * int(line.strip()[:-1])

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
