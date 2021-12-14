import time
start = time.perf_counter()


def get_map(instruction_row):
    group_5 = []
    group_6 = []
    map = {}
    for instruction in instruction_row:
        if len(instruction) == 2:
            map[1] = set(list(instruction))
        elif len(instruction) == 3:
            map[7] = set(list(instruction))
        elif len(instruction) == 4:
            map[4] = set(list(instruction))
        elif len(instruction) == 5:
            group_5.append(set(list(instruction)))
        elif len(instruction) == 6:
            group_6.append(set(list(instruction)))
        elif len(instruction) == 7:
            map[8] = set(list(instruction))

    possible_6 = []
    for t1 in group_6:
        for t2 in group_5:
            if t2.issubset(t1):
                possible_6.append(t1)

    for t in group_6:
        if map[4].issubset(t):
            map[9] = t
        elif t in possible_6:
            map[6] = t
        else:
            map[0] = t

    for t in group_5:
        if t.issubset(map[6]):
            map[5] = t
        elif t.issubset(map[9]):
            map[3] = t
        else:
            map[2] = t

    return map


instructions = []
digits = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        digit_row = []
        instruction_row = []
        digit = ''
        after_sep = False
        for x in row:
            if x in (' ', '\n'):
                if digit != '':
                    if after_sep:
                        digit_row.append(digit)
                    else:
                        instruction_row.append(digit)
                    digit = ''
            elif x == '|':
                after_sep = True
            else:
                digit += x
        digits.append(digit_row)
        instructions.append(instruction_row)

print(sum([1 if len(digit) in (2, 3, 4, 7) else 0 for digit_row in digits for digit in digit_row]))

numbers = []
for row_nr, digit_row in enumerate(digits):
    instruction_row = instructions[row_nr]
    map = get_map(instruction_row)
    m = 1000
    d = 0
    for digit in digit_row:
        t = set(list(digit))
        for i, instruction in map.items():
            if instruction == t:
                d += m * i
                m = m / 10
    numbers.append(d)

print(sum(numbers))

print('time', time.perf_counter()-start)