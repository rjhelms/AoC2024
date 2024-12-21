from time import perf_counter

IN_FILE = "17/input.txt"


class Computer:
    A = 0
    B = 0
    C = 0
    PROG = []
    PC = 0
    OUTPUT = []


def eval_combo(comp, operand):
    if operand < 4:
        return operand
    elif operand == 4:
        return comp.A
    elif operand == 5:
        return comp.B
    elif operand == 6:
        return comp.C
    raise ValueError


def adv(comp: Computer):
    comp.A = int(comp.A / 2 ** (eval_combo(comp, comp.PROG[comp.PC + 1])))
    comp.PC += 2


def bxl(comp: Computer):
    comp.B = comp.B ^ comp.PROG[comp.PC + 1]
    comp.PC += 2


def bst(comp: Computer):
    comp.B = eval_combo(comp, comp.PROG[comp.PC + 1]) % 8
    comp.PC += 2


def jnz(comp: Computer):
    if comp.A == 0:
        comp.PC += 2
        return
    comp.PC = comp.PROG[comp.PC + 1]


def bxc(comp: Computer):
    comp.B = comp.B ^ comp.C
    comp.PC += 2


def out(comp: Computer):
    comp.OUTPUT.append(eval_combo(comp, comp.PROG[comp.PC + 1]) % 8)
    comp.PC += 2


def bdv(comp: Computer):
    comp.B = int(comp.A / 2 ** (eval_combo(comp, comp.PROG[comp.PC + 1])))
    comp.PC += 2


def cdv(comp: Computer):
    comp.C = int(comp.A / 2 ** (eval_combo(comp, comp.PROG[comp.PC + 1])))
    comp.PC += 2


operations = [adv, bxl, bst, jnz, bxc, out, bdv, cdv]

if __name__ == "__main__":
    start_time = perf_counter()

    comp = Computer
    with open(IN_FILE) as f:
        for line in f:
            if len(line.strip()) > 0:
                if line.split()[1] == "A:":
                    comp.A = int(line.split()[-1])
                elif line.split()[1] == "B:":
                    comp.B = int(line.split()[-1])
                elif line.split()[1] == "C:":
                    comp.B = int(line.split()[-1])
                elif line.split()[0] == "Program:":
                    comp.PROG = [int(x) for x in line.split()[1].split(",")]

    while comp.PC < len(comp.PROG):
        operations[comp.PROG[comp.PC]](comp)

    for x in range(len(comp.OUTPUT)):
        print(comp.OUTPUT[x], end="")
        if x < len(comp.OUTPUT) - 1:
            print(",", end="")
    print()

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
