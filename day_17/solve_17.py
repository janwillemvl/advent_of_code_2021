import math
import time
start = time.perf_counter()


class Area:
    def __init__(self, min_x, max_x, min_y, max_y):
        assert(min_x<max_x and min_y<max_y)
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def point_is_in_area(self, x, y):
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def __str__(self):
        return f'x={self.min_x}..{self.max_x}, y={self.min_y}..{self.max_y}'


def get_target_from_string(input_string):
    assert(input_string.startswith('target area: '))
    coord_part = input_string[13:]
    coords = [[int(c) for c in part[2:].split('..')] for part in coord_part.split(', ')]
    return Area(coords[0][0], coords[0][1], coords[1][0], coords[1][1])


def test_shot(vx, vy, target):
    x, y = 0, 0
    max_y = y
    while x <= target.max_x and y >= target.min_y:
        max_y = max(y, max_y)
        if target.point_is_in_area(x, y):
            return max_y
        else:
            x, y = x+vx, y+vy
            vx, vy = max(vx - 1, 0), vy - 1
    return None

target = None
with open('input.txt', 'r') as f_in:
    for row in f_in:
        assert not target
        row = row[:-1] if row[-1] == '\n' else row
        target = get_target_from_string(row)

print(target)

min_n = math.floor(math.sqrt(0.25 + 2 * target.min_x) - 0.5)
max_y = max(target.max_y, -target.min_y)+1

successful_heights = []
for vy in range(-max_y,max_y):
    for vx in range(min_n, target.max_x+1):
        height = test_shot(vx, vy, target)
        if height is not None:
            print(vx, vy, height)
            successful_heights.append(height)

print(f'max height: {max(successful_heights)}')
print(f'number of paths: {len(successful_heights)}')

print('time', time.perf_counter()-start)