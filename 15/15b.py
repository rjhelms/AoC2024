from time import perf_counter
from collections import defaultdict
import os

IN_FILE = "15/input.txt"

MAP = defaultdict(lambda: None)

MOVE_VECTORS = {"^": (0, -1), ">": (1, 0), "v": (0, 1), "<": (-1, 0)}

WORLD_X = 0
WOLRD_Y = 0

VISUALIZE = True


class Tile:
    size = 1
    string = "!"

    def __init__(self, position: tuple[int]):
        self.position = position
        self.register_position()

    def register_position(self):
        for x in range(self.size):
            MAP[self.position[0] + x, self.position[1]] = self

    def clear_position(self):
        for x in range(self.size):
            MAP[self.position[0] + x, self.position[1]] = None

    def try_move(self, direction: str):
        # handle up and downs
        if direction == "^" or direction == "v":
            if direction == "^":
                y_offset = -1
            else:
                y_offset = 1

            # if this is only one tile wide, only need to check one tile
            if self.size == 1:
                check_position = (self.position[0], self.position[1] + y_offset)
                if MAP[check_position] is None:
                    return True
                else:
                    return MAP[check_position].try_move(direction)

            # otherwise build list of tiles to check
            check_tiles = []
            for x in range(self.size):
                check_tiles.append((self.position[0] + x, self.position[1] + y_offset))

            # they might be the same tile - so only need to do one check
            if MAP[check_tiles[0]] is [check_tiles[1]]:
                if MAP[check_tiles[0]] is None:
                    return True
                else:
                    return MAP[check_tiles[0]].try_move(direction)

            # try each tile and return false if it doesn't work
            for tile in check_tiles:
                if MAP[tile] and not MAP[tile].try_move(direction):
                    return False

            # and if we got here, return true
            return True

        # left and right are simple cases
        if direction == "<":
            check_position = (self.position[0] - 1, self.position[1])
        else:
            check_position = (self.position[0] + self.size, self.position[1])
        if MAP[check_position] is None:
            return True
        else:
            return MAP[check_position].try_move(direction)

    def do_move(self, direction: str):
        # try the move - and if it fails, don't do anything
        if not self.try_move(direction):
            return False

        # otherwise this basically looks the same as try_move
        # handle up and downs
        if direction == "^" or direction == "v":
            if direction == "^":
                y_offset = -1
            else:
                y_offset = 1

            # if this is only one tile wide, only need to check one tile
            if self.size == 1:
                check_position = (self.position[0], self.position[1] + y_offset)
                if MAP[check_position] is None:
                    self.clear_position()
                    self.position = check_position
                    self.register_position()
                    return True
                else:
                    if MAP[check_position].do_move(direction):
                        self.clear_position()
                        self.position = check_position
                        self.register_position()
                        return True
                    return False

            # otherwise build list of tiles to check
            check_tiles = []
            for x in range(self.size):
                check_tiles.append((self.position[0] + x, self.position[1] + y_offset))

            # they might be the same tile - so only need to do one check
            if MAP[check_tiles[0]] is [check_tiles[1]]:
                if MAP[check_tiles[0]] is None:
                    self.clear_position()
                    self.position = check_tiles[0]
                    self.register_position()
                    return True
                else:
                    if MAP[check_tiles[0]].do_move(direction):
                        self.clear_position()
                        self.position = check_tiles[0]
                        self.register_position()
                        return True
                    return False

            # try each tile and return false if it doesn't work
            for tile in check_tiles:
                if MAP[tile] and not MAP[tile].do_move(direction):
                    return False
            self.clear_position()
            self.position = check_tiles[0]
            self.register_position()
            return True

        # left and right are simple cases
        if direction == "<":
            check_position = (self.position[0] - 1, self.position[1])
            if MAP[check_position] is None:
                self.clear_position()
                self.position = check_position
                self.register_position()
                return True
            else:
                if MAP[check_position].do_move(direction):
                    self.clear_position()
                    self.position = check_position
                    self.register_position()
                    return True
                return False
        else:
            check_position = (self.position[0] + self.size, self.position[1])
            if MAP[check_position] is None:
                self.clear_position()
                self.position = (self.position[0] + 1, self.position[1])
                self.register_position()
                return True
            else:
                if MAP[check_position].do_move(direction):
                    self.clear_position()
                    self.position = (self.position[0] + 1, self.position[1])
                    self.register_position()
                    return True
                return False

    def string_at_pos(self, position: tuple[int]):
        return self.string

    def __str__(self):
        return self.string


class Wall(Tile):
    size = 2
    string = "█"

    # walls never move
    def try_move(self, direction: str):
        return False

    def do_move(self, direction: str):
        return False


class Box(Tile):
    size = 2
    string = "O"

    def string_at_pos(self, position: tuple[int]):
        if position == self.position:
            return "["
        return "]"


class Robot(Tile):
    string = "☻"
    pass


def draw_map():
    os.system("")
    print("\033[H")
    for y in range(WORLD_Y):
        for x in range(WORLD_X):
            tile = MAP[x, y]
            if tile:
                print(tile.string_at_pos((x, y)), end="")
            else:
                print(" ", end="")
        print()


if __name__ == "__main__":
    start_time = perf_counter()
    world_x = 0
    world_y = 0

    robot = None

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
                        char = line[x]
                        if char == "#":
                            Wall((x * 2, y))
                        elif char == "O":
                            Box((x * 2, y))
                        elif char == "@":
                            robot = Robot((x * 2, y))

                    y += 1
                    WORLD_Y = y
                    WORLD_X = len(line.strip()) * 2

    if VISUALIZE:
        os.system("cls")
        draw_map()

    for char in instructions:
        result = robot.do_move(char)
        if VISUALIZE:
            draw_map()

    score = 0

    checked_boxes = []
    for tile in MAP:
        if isinstance(MAP[tile], Box):
            if MAP[tile] not in checked_boxes:
                score += MAP[tile].position[0] + 100 * MAP[tile].position[1]
                checked_boxes.append(MAP[tile])

    print(score)
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
