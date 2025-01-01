from time import perf_counter
from functools import cache

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


def get_moves(current: str, target: str, pad: dict) -> str:
    position = pad[current]
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
        return "A"
    if x_mov == 0:
        return y_str + "A"
    elif y_mov == 0:
        return x_str + "A"
    else:
        # ensure no path that goes over an empty spot
        if (position[0] == pad[None][0]) and (target_pos[1] == pad[None][1]):
            return x_str + y_str + "A"
        elif (position[1] == pad[None][1]) and (target_pos[0] == pad[None][0]):
            return y_str + x_str + "A"
        else:
            if "<" in x_str:
                return x_str + y_str + "A"
            else:
                return y_str + x_str + "A"


def get_path(current: str, target: str, pad: dict) -> str:
    path = ""
    for char in target:
        path = path + get_moves(current, char, pad)
        current = char
    return path


def get_path_recursive(code, pad_dicts):
    num_levels = len(pad_dicts) - 1

    @cache
    def num_presses(current, target, level):
        sequence = get_path(current, target, pad_dicts[level])
        if level == num_levels:
            return len(sequence)
        else:
            length = 0
            current = "A"
            for target in sequence:
                length += num_presses(current, target, level + 1)
                current = target
            return length

    length = 0
    current = "A"
    for target in code:
        length += num_presses(current, target, 0)
        current = target
    print(code, length)
    return length


if __name__ == "__main__":
    start_time = perf_counter()

    pad_dicts = [NUM_PAD_POSITIONS]
    for i in range(25):
        pad_dicts.append(DIR_PAD_POSITIONS)

    score = 0

    with open(IN_FILE) as f:
        for line in f:
            length = get_path_recursive(line.strip(), pad_dicts)
            score += length * int(line.strip()[:-1])

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
