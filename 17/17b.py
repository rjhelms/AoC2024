from time import perf_counter
from copy import deepcopy

IN_FILE = "17/input.txt"


class Computer:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.PROG = []
        self.PC = 0
        self.OUTPUT = []


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

    start_comp = Computer()
    with open(IN_FILE) as f:
        for line in f:
            if len(line.strip()) > 0:
                if line.split()[1] == "A:":
                    start_comp.A = int(line.split()[-1])
                elif line.split()[1] == "B:":
                    start_comp.B = int(line.split()[-1])
                elif line.split()[1] == "C:":
                    start_comp.B = int(line.split()[-1])
                elif line.split()[0] == "Program:":
                    start_comp.PROG = [int(x) for x in line.split()[1].split(",")]

    test_A = 35184372088832  # minimum value that will produce 16 char output

    while True:
        test_comp = deepcopy(start_comp)
        test_comp.A = test_A
        test_comp_valid = True
        while test_comp.PC < len(test_comp.PROG):
            operations[test_comp.PROG[test_comp.PC]](test_comp)

        # output is cyclical, with index N changing every 8 ** n iterations
        # each step, increase value by amount required to change last incorrect digit

        increase = 0
        for i in range(len(test_comp.OUTPUT)):
            if test_comp.OUTPUT[15 - i] != test_comp.PROG[15 - i]:
                increase = 8 ** (15 - i)
                break

        if test_comp.OUTPUT == test_comp.PROG:
            print(test_A)
            break
        test_A += increase

    end_time = perf_counter()
    print(f"Execution time: {end_time-start_time:.3f}s")
