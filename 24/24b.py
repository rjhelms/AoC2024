from time import perf_counter

IN_FILE = "24/input.txt"

# known wires just hold values
KNOWN_WIRES = {}

# unknown wires hold tuple - (first, second, operation)
UNKNOWN_WIRES = {}

"""
cool ASCII art rendering of adders

x00  --------X---
             |   XOR ---- z00
y00  ---X----+---
	|    |
	|    +---
	|        AND ---- c00 (real name unknown)
	+--------
	
	
x01  --------X---      t01 (real name unknown)
             |   XOR ------x
y01  ---X----+---          x-----
        |    |             |    XOR ------- z01
c00 ----+----+---------x---------
        |    |         |   |
        |    |         |   +----     a01
        |    |         |        AND --+
        |    |         +---c00--      |
        |    |                         OR - c01 (real name unknown)
        |    +--------x01-------      |
        |                       AND --+
        +-------------y01-------     b01

from this - can identify what each wire "actually" is and see wires that go the wrong place
"""

if __name__ == "__main__":
    start_time = perf_counter()

    with open(IN_FILE) as f:
        for line in f:
            if ":" in line:
                line = line.split(":")
                KNOWN_WIRES[line[0]] = int(line[1])
            elif "->" in line:
                line = [x.split() for x in line.split(" -> ")]
                UNKNOWN_WIRES[line[1][0]] = (line[0][0], line[0][2], line[0][1])

    mappings = {}
    swaps = []

    # perform initial mappings
    mappings["x00"] = "x00"
    mappings["y00"] = "y00"

    # only thing accomplished here is identifying the carry wire
    for wire in UNKNOWN_WIRES:
        if (
            "x00" in UNKNOWN_WIRES[wire]
            and "y00" in UNKNOWN_WIRES[wire]
            and UNKNOWN_WIRES[wire][2] == "XOR"
        ):
            mappings["z00"] = wire
        elif (
            "x00" in UNKNOWN_WIRES[wire]
            and "y00" in UNKNOWN_WIRES[wire]
            and UNKNOWN_WIRES[wire][2] == "AND"
        ):
            mappings["c00"] = wire

    # for each gate, go through the mappings
    for i in range(1, int(len(KNOWN_WIRES) / 2)):
        idx_string = f"{i:02d}"
        carry_string = f"{i-1:02d}"

        new_mappings = {}
        new_mappings["x" + idx_string] = "x" + idx_string
        new_mappings["y" + idx_string] = "y" + idx_string

        # first find the gates fed by the x and y inputs
        for wire in UNKNOWN_WIRES:
            if (
                "x" + idx_string in UNKNOWN_WIRES[wire]
                and "y" + idx_string in UNKNOWN_WIRES[wire]
                and UNKNOWN_WIRES[wire][2] == "XOR"
            ):
                new_mappings["t" + idx_string] = wire
            elif (
                "x" + idx_string in UNKNOWN_WIRES[wire]
                and "y" + idx_string in UNKNOWN_WIRES[wire]
                and UNKNOWN_WIRES[wire][2] == "AND"
            ):
                new_mappings["b" + idx_string] = wire

        # then the ones fed by the carry flag - one of these should be the output
        for wire in UNKNOWN_WIRES:
            if (
                new_mappings["t" + idx_string] in UNKNOWN_WIRES[wire]
                and mappings["c" + carry_string] in UNKNOWN_WIRES[wire]
                and UNKNOWN_WIRES[wire][2] == "XOR"
            ):
                new_mappings["z" + idx_string] = wire
            elif (
                new_mappings["t" + idx_string] in UNKNOWN_WIRES[wire]
                and mappings["c" + carry_string] in UNKNOWN_WIRES[wire]
                and UNKNOWN_WIRES[wire][2] == "AND"
            ):
                new_mappings["a" + idx_string] = wire

        # if didn't find the output, there's a swap needed with one of the gates feeding the the output, so check those
        if "z" + idx_string not in new_mappings:
            for gate in UNKNOWN_WIRES["z" + idx_string][0:2]:
                new_swaps = []

                # see if we've identified one of them already
                new_key = [i for i in new_mappings if new_mappings[i] == gate]
                old_key = [i for i in mappings if mappings[i] == gate]

                # if it's in the new mapping, it should be the t gate - so do that swap
                if len(new_key) > 0:
                    if "t" not in new_key[0]:
                        new_swaps.append(new_mappings[new_key[0]])
                        new_swaps.append(new_mappings["t" + new_key[0][1:]])
                        print("cross swapping", new_swaps)
                        tmp = new_mappings[new_key[0]]
                        new_mappings[new_key[0]] = new_mappings["t" + new_key[0][1:]]
                        new_mappings["t" + new_key[0][1:]] = tmp
                        left_gate = UNKNOWN_WIRES[new_swaps[1]]
                        right_gate = UNKNOWN_WIRES[new_swaps[0]]
                        UNKNOWN_WIRES[new_swaps[0]] = left_gate
                        UNKNOWN_WIRES[new_swaps[1]] = right_gate
                        swaps.extend(new_swaps)
                elif len(old_key) > 0:
                    if "c" not in old_key[0]:
                        # this case does not arise so didn't handle it - not sure if possible
                        print("old key invalid")

                # and then recheck the ones fed by the carry flag now that this swap is done
                for wire in UNKNOWN_WIRES:
                    if (
                        new_mappings["t" + idx_string] in UNKNOWN_WIRES[wire]
                        and mappings["c" + carry_string] in UNKNOWN_WIRES[wire]
                        and UNKNOWN_WIRES[wire][2] == "XOR"
                    ):
                        new_mappings["z" + idx_string] = wire
                    elif (
                        new_mappings["t" + idx_string] in UNKNOWN_WIRES[wire]
                        and mappings["c" + carry_string] in UNKNOWN_WIRES[wire]
                        and UNKNOWN_WIRES[wire][2] == "AND"
                    ):
                        new_mappings["a" + idx_string] = wire

        # other case could be that the output wire itself is in the wrong place
        # in this case, we know what wire *should* be the output wire
        elif new_mappings["z" + idx_string] != "z" + idx_string:
            new_swaps = []
            new_swaps.append(new_mappings["z" + idx_string])
            new_swaps.append("z" + idx_string)
            # perform the swap in the tree
            left_gate = UNKNOWN_WIRES[new_swaps[1]]
            right_gate = UNKNOWN_WIRES[new_swaps[0]]
            UNKNOWN_WIRES[new_swaps[0]] = left_gate
            UNKNOWN_WIRES[new_swaps[1]] = right_gate

            # three possible cases - place to swap is in the current tier, already passed, or haven't found yet
            new_key = [i for i in new_mappings if new_mappings[i] == "z" + idx_string]
            old_key = [i for i in mappings if mappings[i] == "z" + idx_string]
            if len(new_key) > 0:
                print("new swapping", new_swaps)
                new_mappings["z" + idx_string] = new_swaps[1]
                new_mappings[new_key[0]] = new_swaps[0]
            elif len(old_key) > 0:
                # this case does not arise - not sure if it's possible
                print("old swapping", new_swaps)
                new_mappings["z" + idx_string] = new_swaps[1]
                mappings[old_key[0]] = new_swaps[0]
            else:
                # swap handled entirely by unknown wires above
                print("future swapping", new_swaps)
                new_mappings["z" + idx_string] = new_swaps[1]
            swaps.extend(new_swaps)

        # finally, identify carry wire
        for wire in UNKNOWN_WIRES:
            if (
                new_mappings["a" + idx_string] in UNKNOWN_WIRES[wire]
                and new_mappings["b" + idx_string] in UNKNOWN_WIRES[wire]
                and UNKNOWN_WIRES[wire][2] == "OR"
            ):
                new_mappings["c" + idx_string] = wire
        mappings.update(new_mappings)

    swaps.sort()
    str = ""
    for gate in swaps:
        str += gate
        str += ","

    print(str[:-1])
    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
