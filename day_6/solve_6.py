import time
t = time.perf_counter()
fishes = {0:{}}
with open('input.txt', 'r') as f_in:
    for row in f_in:
        for x in row:
            if x is not ',':
                x = int(x)
                fishes[0][x] = fishes[0][x] + 1 if x in fishes[0] else 1

n_days = 256
for i in range(1, n_days+1):
    fishes[i] = {i-1: n for (i, n) in fishes[i-1].items() if i > 0}
    if 0 in fishes[i - 1]:
        fishes[i][6] = fishes[i-1][0] + (fishes[i][6] if 6 in fishes[i] else 0)
        fishes[i][8] = fishes[i-1][0]
print(sum(fishes[n_days].values()))
print(time.perf_counter()-t)
