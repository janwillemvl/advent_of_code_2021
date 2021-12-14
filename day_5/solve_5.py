# create class Line
class Point:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.key = 1000000 * self.x + self.y

    @classmethod
    def from_numbers(cls, x, y):
        return cls(x, y)

    @classmethod
    def from_string(cls, point_string):
        point_list = point_string.split(',')
        assert(len(point_list) == 2)
        return cls(point_list[0], point_list[1])


class Line:
    def __init__(self, line_string):
        line_list = line_string.split(' -> ')
        assert(len(line_list) == 2)
        self.start = Point.from_string(line_list[0])
        self.stop = Point.from_string(line_list[1])
        if self.start.x == self.stop.x:
            x = self.start.x
            y0 = min(self.start.y, self.stop.y)
            y1 = max(self.start.y, self.stop.y)
            self.points = [Point.from_numbers(x, yi) for yi in range(y0, y1 + 1, 1)]
        elif self.start.y == self.stop.y:
            y = self.start.y
            x0 = min(self.start.x, self.stop.x)
            x1 = max(self.start.x, self.stop.x)
            self.points = [Point.from_numbers(xi, y) for xi in range(x0, x1 + 1, 1)]
        else:
            self.points = []
            dx = 1 if self.start.x < self.stop.x else -1
            dy = 1 if self.start.y < self.stop.y else -1
            xi = self.start.x
            yi = self.start.y
            while xi != self.stop.x and yi != self.stop.y:
                self.points.append(Point.from_numbers(xi, yi))
                xi += dx
                yi += dy
            assert(xi == self.stop.x and yi == self.stop.y)
            self.points.append(Point.from_numbers(xi, yi))


    def __contains__(self, item):
        assert(type(item)==Point)
        return min(self.start.x, self.stop.x) <= item.x <= max(self.start.x, self.stop.x) \
        and min(self.start.y, self.stop.y) <= item.y <= max(self.start.y, self.stop.y)


lines = []
points = {}
with open('input.txt', 'r') as file_in:
    for row in file_in:
        line = Line(row[:-1])
        lines.append(line)
        for point in line.points:
            if point.key not in points.keys():
                points[point.key] = 1
            else:
                points[point.key] += 1

s = len([key for key, value in points.items() if value > 1])
print(max(points.keys()))
print(s)


# parse input to lines