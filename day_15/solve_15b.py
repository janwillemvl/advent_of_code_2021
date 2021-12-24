import time
start = time.perf_counter()
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

plt.ion()


class PathKeeper:
    def __init__(self, x, y, start_value, risk_levels):
        self.coordinate_list = [(x,y)]
        self.value_list = [start_value]
        self.prev_paths = {(x,y): start_value}
        self.risk_levels = risk_levels
        self.size = len(risk_levels)
        self.solution = None
        self.matrix = np.zeros([self.size, self.size], dtype=np.uint8)
        self.matrix[4,4] = 10

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.im = self.ax.imshow(self.matrix, vmin=0, vmax=10)
        plt.show(block=True)

        plt.draw()
        plt.pause(1)

    def get_neighbours(self, x, y, value):
        neighbours = []
        if x > 0:
            neighbours.append(((x-1, y), self.risk_levels[y][x - 1] + value))
        if y > 0:
            neighbours.append(((x, y-1), self.risk_levels[y - 1][x] + value))
        if x < self.size - 1:
            neighbours.append(((x+1, y), self.risk_levels[y][x + 1] + value))
        if y < self.size - 1:
            neighbours.append(((x, y+1), self.risk_levels[y + 1][x] + value))

        return neighbours

    def next_step(self):
        coordinates = self.coordinate_list.pop(0)
        value = self.value_list.pop(0)
        neighbours = self.get_neighbours(*coordinates, value)
        for n in neighbours:
            if n[0] == (self.size-1, self.size-1):
                # done!
                self.solution = n[1]
                break
            elif n[0] not in self.prev_paths.keys():
                index = 0
                for i, v in enumerate(self.value_list):
                    if v >= n[1]:
                        break
                    index = i + 1
                self.value_list.insert(index, n[1])
                self.coordinate_list.insert(index, n[0])
                self.prev_paths[n[0]] = n[1]
                self.matrix[n[0][0], n[0][1]] = n[1]
        self.update_plot()

    def solve(self):
        counter = 0
        while not self.solution:
            self.next_step()
            counter += 1
        return self.solution

    def update_plot(self):
        self.im.set_array(self.matrix)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        plt.pause(0.0001)


risk_levels = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        risk_levels.append([int(c) for c in row if c != '\n'])

p = PathKeeper(0, 0, 0, risk_levels)
solution = p.solve()
print(solution)

extended_risk_levels = risk_levels.copy()
factor = 5
size = len(risk_levels)

for y in range(factor * size):
    if y >= size:
        extended_risk_levels.append(extended_risk_levels[y-size][size:].copy())
    for x in range(factor * size):
        if x >= len(extended_risk_levels[y]):
            extended_risk_levels[y].append((extended_risk_levels[y][x-size] % 9)+1)

#p = PathKeeper(0, 0, 0, extended_risk_levels)
#solution = p.solve()
#print(solution)

plt.show()

print('time', time.perf_counter()-start)