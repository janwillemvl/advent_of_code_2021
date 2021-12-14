
def get_decimal_from_binary(binary):
    return sum([(2**(len(binary)-i-1))*x for i, x in enumerate(binary)])

print(get_decimal_from_binary([1,1,0,0,1])) # 1+8+16 = 25

input_list = []
with open('input.txt') as f:
    input_list = [row[:-1] for row in f]


def get_gamma_and_epsilon_bits(input_list):
    counter = [0] * (len(input_list[0]))
    size = len(input_list)
    for row in input_list:
        for pos, bit in enumerate(row):
            counter[pos] += int(bit)

    gamma_bits = [round((s+0.1)/size) for s in counter]
    epsilon_bits = [1-x for x in gamma_bits]
    return gamma_bits, epsilon_bits


gamma_bits, epsilon_bits = get_gamma_and_epsilon_bits(input_list)

gamma = get_decimal_from_binary(gamma_bits)
epsilon = get_decimal_from_binary(epsilon_bits)

print(gamma*epsilon)

o2_list, co2_list = input_list, input_list
for i in range(len(gamma_bits)):
    print(i)
    if len(o2_list) > 1:
        o2_bits, _ = get_gamma_and_epsilon_bits(o2_list)
        o2_list = [row for row in o2_list if int(row[i]) == o2_bits[i]]

    if len(co2_list) > 1:
        _, co2_bits = get_gamma_and_epsilon_bits(co2_list)
        co2_list = [row for row in co2_list if int(row[i]) == co2_bits[i]]

o2_rating = get_decimal_from_binary([int(x) for x in o2_list[0]])
co2_rating = get_decimal_from_binary([int(x) for x in co2_list[0]])

print(o2_rating * co2_rating)


