import time
start = time.perf_counter()


class Cave:
    def __init__(self, key):
        self.key = key
        self.linked_caves = []

    def add_link(self, cave):
        self.linked_caves.append(cave)

    def should_visit(self, linked_cave, journey_so_far, rule):
        if linked_cave.key == 'start':
            return False
        if rule == 'once':
            return linked_cave.is_big() or linked_cave.key not in journey_so_far
        elif rule == 'twice':
            if linked_cave.is_big() or linked_cave.key not in journey_so_far:
                return True
            elif journey_so_far.count(linked_cave.key) == 1:
                return True

    def traverse(self, journey_so_far, rule='once'):
        if rule == 'twice' and not self.is_big() and self.key in journey_so_far:
            rule = 'once'
        journey_so_far.append(self.key)
        if self.key == 'end':
            return [journey_so_far]
        journeys = []
        for cave in self.linked_caves:
            should_visit = self.should_visit(cave, journey_so_far, rule)
            if should_visit:
                journey_next = journey_so_far.copy()
                journeys.extend(cave.traverse(journey_next, rule))
        return journeys

    def is_big(self):
        return self.key == self.key.upper()

    def __str__(self):
        return self.key


class CaveSystem:
    def __init__(self, description):
        self.caves = {}
        for line in description:
            cave_keys = line.split('-')
            for cave_key in cave_keys:
                if cave_key not in self.caves.keys():
                    self.caves[cave_key] = Cave(cave_key)
            self.add_link(self.caves[cave_keys[0]], self.caves[cave_keys[1]])

    def add_link(self, cave_1, cave_2):
        cave_1.add_link(cave_2)
        cave_2.add_link(cave_1)

    def traverse(self, rule):
        assert('start' in self.caves.keys() and 'end' in self.caves.keys())
        start_cave = self.caves['start']
        start_journey = []
        journeys = start_cave.traverse(start_journey, rule)
        for journey in journeys:
            print(','.join(journey))
        print(len(journeys))


input = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        input.append(row[:-1] if row[-1] == '\n' else row)

system = CaveSystem(input)
system.traverse('once')
system.traverse('twice')

print('time', time.perf_counter()-start)