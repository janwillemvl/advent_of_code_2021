import time
start = time.perf_counter()

octopi = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        octopi.append([int(c) for c in row if c != '\n'])

n_octopi = sum([len(row) for row in octopi])
print(f'there are {n_octopi} octopuses.')


def flash(octopi, i, j):
    octopi[i][j] = 0
    for l in range(j-1, j+2):
        for k in range(i-1, i+2):
            if 0<=l<len(octopi) and 0<=k<len(octopi[l]) and octopi[k][l] > 0:
                octopi[k][l] += 1
                if octopi[k][l] > 9:
                    flash(octopi, k, l)


def simulate_step(octopi):
    # first increase all by one
    for j, row in enumerate(octopi):
        for i, col in enumerate(row):
            octopi[i][j] += 1

    # the do the flashes
    for j, row in enumerate(octopi):
        for i, col in enumerate(row):
            if octopi[i][j] > 9:
                flash(octopi, i, j)


def simulate(octopi, steps):
    total_flashes = []
    for step in range(steps):
        simulate_step(octopi)
        flashes = sum([len([x for x in row if x == 0]) for row in octopi])
        if flashes == n_octopi:
            print('all octopuses flash at step: ', step + 1)
            break
        total_flashes.append(flashes)

    return sum(total_flashes)


print(simulate(octopi, 1000))

print('time', time.perf_counter()-start)