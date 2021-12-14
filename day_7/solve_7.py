import time
import statistics
import json
t = time.perf_counter()

crabs = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        crabs = json.loads('['+row+']')

print(len(crabs))
mean = statistics.mean(crabs)
for x in range(min(crabs), max(crabs), 1):
    s = sum([0.5*abs(c-x)*(abs(c-x)+1) for c in crabs])
    print(x, s)

print(mean)
x = mean
s = sum([0.5*abs(c-x)*(abs(c-x)+1) for c in crabs])
print(mean, s)

print(time.perf_counter()-t)
