import time
start = time.perf_counter()


def get_cum_risk_level(cum_risk_levels, risk_levels, x, y):
    neighbours = []
    if x == 0 and y == 0:
        return 0
    if x > 0:
        neighbours.append(cum_risk_levels[y][x-1])
    if y > 0:
        neighbours.append(cum_risk_levels[y-1][x])
    if x < len(cum_risk_levels[y]) - 1:
        neighbours.append(cum_risk_levels[y][x+1])
    if y < len(cum_risk_levels) - 1:
        neighbours.append(cum_risk_levels[y+1][x])

    return min(neighbours) + risk_levels[y][x]


risk_levels = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        risk_levels.append([int(c) for c in row if c != '\n'])


def get_lowest_risk(risk_levels):
    size = len(risk_levels)
    cum_risk_levels = list()
    for y, row in enumerate(risk_levels):
        assert(len(row) == size)
        cum_risk_levels.append(list())
        for x, col in enumerate(row):
            cum_risk_levels[y].append(get_cum_risk_level(cum_risk_levels, risk_levels, x, y))

    loops = 10
    for i in range(loops):
        for x in range(size):
            for y in range(size):
                cum_risk_levels[y][x] = get_cum_risk_level(cum_risk_levels, risk_levels, x, y)

    return cum_risk_levels[-1][-1]


print(get_lowest_risk(risk_levels))

extended_risk_levels = risk_levels.copy()
factor = 5
size = len(risk_levels)

for y in range(factor * size):
    if y >= size:
        extended_risk_levels.append(extended_risk_levels[y-size][size:].copy())
    for x in range(factor * size):
        if x >= len(extended_risk_levels[y]):
            extended_risk_levels[y].append((extended_risk_levels[y][x-size]%9)+1)

print(get_lowest_risk(extended_risk_levels))

print('time', time.perf_counter()-start)