import time
start = time.perf_counter()

height_map = {}
low_in_row = {}
with open('input.txt', 'r') as f_in:
    for i, row in enumerate(f_in):
        height_map[i] = {}
        low_in_row[i] = {}
        rolling_triplet = [10, 10, 10]
        for j, c in enumerate(row):
            if c != '\n':
                x = int(c)
                rolling_triplet = rolling_triplet[1:] + [x]
                if rolling_triplet[1] < min(rolling_triplet[0], x):
                    low_in_row[i][j-1] = rolling_triplet[1]
                height_map[i][j] = x
            else:
                rolling_triplet = rolling_triplet[1:]
                if rolling_triplet[1] < rolling_triplet[0]:
                    low_in_row[i][j-1] = rolling_triplet[1]


low_points = {}
for row_nr, row in low_in_row.items():
    low_points[row_nr] = {}
    for index, value in row.items():
        is_low = True
        if row_nr > 0:
            if height_map[row_nr-1][index] <= value:
                is_low = False
        if row_nr < len(height_map.keys()) - 1:
            if height_map[row_nr+1][index] <= value:
                is_low = False
        if is_low:
            low_points[row_nr][index] = value

s = sum([sum(row.values()) + len(row.values()) for row in low_points.values()])
print('risk: ', s)

max_cols = max([len(row.keys()) for row in height_map.values()])


def get_cell_id(x, y, max_cols):
    return y*max_cols + x


def add_basin_members(height_map, x, y, max_cols, basin):
    if y in height_map.keys() and x in height_map[y].keys() and height_map[y][x] < 9:
        id = get_cell_id(x, y, max_cols)
        if id not in basin:
            basin.add(id)
            for i in range(-1, 2, 1):
                for j in range(-1, 2, 1):
                    if i == 0 or j == 0:
                        add_basin_members(height_map, x + i, y + j, max_cols, basin)

    return basin


basins = {}
for row_nr, row in low_points.items():
    for index, value in row.items():
        cell_id = get_cell_id(index, row_nr, max_cols)
        basins[cell_id] = add_basin_members(height_map, index, row_nr, max_cols, set())

sizes = [len(points) for id, points in basins.items()]
sizes = sorted(sizes)
print('basin sizes: ', sizes)
print('product of biggest three: ', (sizes[-1] * sizes[-2] * sizes[-3]))

print('time', time.perf_counter()-start)