import time
start = time.perf_counter()


hex_binary_map = {
    '0' : '0000',
    '1' : '0001',
    '2' : '0010',
    '3' : '0011',
    '4' : '0100',
    '5' : '0101',
    '6' : '0110',
    '7' : '0111',
    '8' : '1000',
    '9' : '1001',
    'A' : '1010',
    'B' : '1011',
    'C' : '1100',
    'D' : '1101',
    'E' : '1110',
    'F' : '1111'
}

input = []
with open('input.txt', 'r') as f_in:
    for row in f_in:
        input.append(row[:-1] if row[-1] == '\n' else row)

binary_strings = []
for row in input:
    binary = []
    for c in row:
        binary.append(hex_binary_map[c])
    binary_strings.append(''.join(binary))


def binary_to_decimal(binary):
    result = 0
    factor = 1
    for bit in binary[::-1]:
        if bit == '1':
            result += factor
        factor = factor * 2
    return result


def parse_packet_header(packet):
    print(packet)
    version = binary_to_decimal(packet[0:3])
    type_id = binary_to_decimal(packet[3:6])
    content = packet[6:]
    return version, type_id, content


def parse_literal_value(content):
    last_bits = False
    read_bits = False
    bit_count = 0
    result = 0
    bits = ''
    unparsed = ''
    for bit in content:
        if read_bits:
            bits += bit
            bit_count += 1
            if bit_count == 4:
                bit_count = 0
                read_bits = False
        elif last_bits:
            unparsed += bit
        elif bit == '1':
            read_bits = True
        elif bit == '0':
            last_bits = True
            read_bits = True
    if len(bits) > 0:
        result = binary_to_decimal(bits)
    return result, unparsed


def parse_packet(packet):
    packets = []
    version, type_id, unparsed = parse_packet_header(packet)
    if type_id == 4:
        value, unparsed = parse_literal_value(unparsed)
        packets.append(value)
    else:
        length_type_id, unparsed = unparsed[0], unparsed[1:]
        if length_type_id == '0':
            sub_packet_length, unparsed = binary_to_decimal(unparsed[:15]), unparsed[15:]
            sub_packet_binary, unparsed = unparsed[:sub_packet_length], unparsed[sub_packet_length:]
            while len(sub_packet_binary) > 0:
                sub_packets, sub_packet_binary = parse_packet(sub_packet_binary)
                packets.append(sub_packets)
        else:
            sub_packet_number, unparsed = binary_to_decimal(unparsed[:11]), unparsed[11:]
            for i in range(sub_packet_number):
                sub_packets, unparsed = parse_packet(unparsed)
                packets.append(sub_packets)

    return [version, type_id, packets], unparsed


packets = []
for b in binary_strings:
    parsed_packets, unparsed = parse_packet(b)
    packets.extend(parsed_packets)

print('parsed: ', packets)
print('not parsed: ', unparsed)


def get_version_sum(packets):
    if type(packets) == list:
        s = packets[0] if type(packets[0]) == int and len(packets) == 3 else 0
        for packet in packets:
            s += get_version_sum(packet)
    else:
        s = 0
    return s


print(get_version_sum(packets))


def get_sum(packets):
    return sum([get_value(packet) for packet in packets])


def get_product(packets):
    p = 1
    for packet in packets:
        p = p*get_value(packet)
    return p


def get_minimum(packets):
    m = None
    for packet in packets:
        value = get_value(packet)
        m = value if not m else min(m, value)
    return m


def get_maximum(packets):
    m = None
    for packet in packets:
        value = get_value(packet)
        m = value if not m else max(m, value)
    return m


def get_greater_than(packets):
    assert(len(packets) == 2)
    return 1 if get_value(packets[0]) > get_value(packets[1]) else 0


def get_less_than(packets):
    return 1 if get_value(packets[0]) < get_value(packets[1]) else 0


def get_equal_to(packets):
    return 1 if get_value(packets[0]) == get_value(packets[1]) else 0


def get_value(packets):
    if type(packets) != list:
        assert(type(packets) == int)
        return packets
    else:
        if len(packets) == 1:
            return packets[0]
        elif len(packets) == 3:
            type_id = packets[1]
            sub_packets = packets[2]
            if type_id == 0:
                return get_sum(sub_packets)
            elif type_id == 1:
                return get_product(sub_packets)
            elif type_id == 2:
                return get_minimum(sub_packets)
            elif type_id == 3:
                return get_maximum(sub_packets)
            elif type_id == 4:
                return get_value(sub_packets)
            elif type_id == 5:
                return get_greater_than(sub_packets)
            elif type_id == 6:
                return get_less_than(sub_packets)
            elif type_id == 7:
                return get_equal_to(sub_packets)
            else:
                raise ValueError(f'Invalid type id {type} found.')


print(get_value(packets))

print('time', time.perf_counter()-start)

