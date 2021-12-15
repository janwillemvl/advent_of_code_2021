import time
start = time.perf_counter()


def add_key_value_to_dict(polymer, pair, value=1):
    if pair not in polymer.keys():
        polymer[pair] = value
    else:
        polymer[pair] += value
    return polymer


def calculate_minmax_difference(polymer, first, last):
    occurrences = {}
    for key, value in polymer.items():
        for c in key:
            occurrences = add_key_value_to_dict(occurrences, c, value/2)
    occurrences = add_key_value_to_dict(occurrences, first, 1/2)
    occurrences = add_key_value_to_dict(occurrences, last, 1/2)
    return max(list(occurrences.values())) - min(list(occurrences.values()))


polymer = {}
instructions = {}
first, last = '', ''
with open('input.txt', 'r') as f_in:
    for row in f_in:
        row = row[:-1] if '\n' in row else row
        if len(polymer) == 0:
            prev_char = ''
            for i, c in enumerate(row):
                if i == 0:
                    first = c
                else:
                    if i == len(row) - 1:
                        last = c
                    pair = prev_char + c
                    polymer = add_key_value_to_dict(polymer, pair)
                prev_char = c
        elif row != '':
            instruction = row.split(' -> ')
            assert(instruction[0] not in instructions.keys())
            assert(len(instruction[0]) == 2 and len(instruction[1]) == 1)
            instructions[instruction[0]] = (instruction[0][0] + instruction[1], instruction[1] + instruction[0][1])

print(polymer)
assert(len([key for key in polymer.keys() if key in instructions.keys()]) == len(polymer.keys()))
print(instructions)

n_steps = 1000
for i in range(n_steps):
    temp_polymer = {}
    for key, value in polymer.items():
        for new_key in instructions[key]:
            temp_polymer = add_key_value_to_dict(temp_polymer, new_key, value)

    polymer = temp_polymer.copy()
    print(f'step: {i + 1}:')
    print(f'polymer length: {sum(list(polymer.values())) + 1}')
    print(f'minmax diff: {calculate_minmax_difference(polymer, first, last)}')


print('time', time.perf_counter()-start)