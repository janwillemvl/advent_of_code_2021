import time
start = time.perf_counter()

bracket_map = {'[': ']', '(': ')', '{': '}', '<': '>'}
corrupt_score_map = {']': 57, ')': 3, '}': 1197, '>': 25137}
incomplete_score_map = {']': 2, ')': 1, '}': 3, '>': 4}
corrupt_score = 0
incomplete_score_list = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        expected = []
        for c in row:
            if c in bracket_map.keys():
                expected.append(bracket_map[c])
            else:
                if c == expected[-1]:
                    expected = expected[:-1]
                elif c in corrupt_score_map.keys():
                    corrupt_score += corrupt_score_map[c]
                    print('corrupt ', corrupt_score)
                    break
                elif c == '\n':
                    incomplete_score = 0
                    expected.reverse()
                    for x in expected:
                        incomplete_score = incomplete_score * 5 + incomplete_score_map[x]
                    incomplete_score_list.append(incomplete_score)
                    print('incomplete ', incomplete_score)
                else:
                    raise Exception('unexpected character found')

print(sorted(incomplete_score_list)[int(len(incomplete_score_list)/2)])

print('time', time.perf_counter()-start)