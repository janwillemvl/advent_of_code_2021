import time
start = time.perf_counter()

points = []
folds = []
with open('input.txt', 'r') as f_in:
    point_line = True
    for row in f_in:
        row = row[:-1] if '\n' in row else row
        if row == '':
            point_line = False
        else:
            if point_line:
                point = row.split(',')
                point = (int(point[0]), int(point[1]))
                points.append(point)
            else:
                fold = row.split('=')
                fold = [fold[0][-1], int(fold[1])]
                folds.append(fold)


def fold_point(direction, distance, point):
    if direction == 'y':
        return point[0], min(2*distance - point[1], point[1])
    elif direction == 'x':
        return min(2*distance - point[0], point[0]), point[1]
    else:
        raise ValueError(f'invalid direction {direction}')


def fold_points(fold, points):
    new_points = set()
    for point in points:
        new_points.add(fold_point(direction=fold[0], distance=fold[1], point=point))
    return list(new_points)


print(points)
print(folds)

points_1 = fold_points(folds[0], points)
print(f'{len(points_1)} points remaining: {points_1}')

temp_points = points
for fold in folds:
    temp_points = fold_points(fold, temp_points)


def draw(points):
    max_x = 0
    max_y = 0
    for point in points:
        max_x = max(max_x, point[0])
        max_y = max(max_y, point[1])

    for y in range(max_y + 1):
        line = ''
        for x in range(max_x+1):
            if (x,y) in points:
                line += '#'
            else:
                line += '.'
        print(line)


draw(temp_points)

print('time', time.perf_counter()-start)