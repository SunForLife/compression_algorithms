from decimal import Decimal, getcontext
import _pickle as pickle
import sys


ALPHABET_SIZE = 128
MULTIPLICATOR = 1.3
STEP_SIZE = 2000


def read_data(file_name):
    file = open(file_name, mode='r')
    data = file.read()
    file.close()
    return data

def write_data(data, file_name):
    file = open(file_name, mode='w')
    file.write(data)
    file.close()
    return

def read_encoded_data(file_name):
    return

def count_frequencies(data):
    frequencies = [0] * ALPHABET_SIZE
    for c in data:
        frequencies[ord(c)] += 1
    return frequencies

def count_intervals(frequencies):
    intervals = []
    curs = Decimal(0)
    alls = Decimal(sum(frequencies))
    for i in range(ALPHABET_SIZE):
        curs += frequencies[i]
        left = Decimal(0.0)
        if i > 0:
            left = intervals[i - 1][1]
        intervals.append((left, curs / alls))
    return intervals

def encode(data, frequencies):
    intervals = count_intervals(frequencies)
    left, right = Decimal(0.0), Decimal(1.0)

    for c in data:
        new_left = left + (right - left) * intervals[ord(c)][0]
        right = left + (right - left) * intervals[ord(c)][1]
        left = new_left

    return (left + right) / 2

def decode(encoded_value, frequencies, data_len):
    intervals = count_intervals(frequencies)
    data = ""
    left, right = Decimal(0.0), Decimal(1.0)

    for i in range(data_len):
        for j in range(ALPHABET_SIZE):
            cur_left = left + (right - left) * intervals[j][0]
            if cur_left > encoded_value:
                continue
            cur_right = left + (right - left) * intervals[j][1]
            if cur_right < encoded_value:
                continue
            data += chr(j)
            left = cur_left
            right = cur_right
            break

    return data

def decimal_to_string(dec):
    dec_str = str(dec)
    ret = ''
    for i in range(len(dec_str)):
        ret += dec_str[i]
        if dec_str[i] == '.':
            for j in range(i + 1, len(dec_str), 2):
                ret += chr(int(dec_str[j:j+2]))
            break
    return ret

def string_to_decimal(s):
    dec_str = ''
    for i in range(len(s)):
        dec_str += s[i]
        if s[i] == '.':
            for j in range(i + 1, len(s)):
                if len(str(ord(s[j]))) == 1:
                    dec_str += '0'
                dec_str += str(ord(s[j]))
            break
    return Decimal(dec_str)

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output)

def load_object(filename):
    with open(filename, 'rb') as inputt:
        return pickle.load(inputt)

class Value:
    def __init__(self, encoded_value, frequencies, data_len):
        self.encoded_value = encoded_value
        self.frequencies = frequencies
        self.data_len = data_len

def main():
    if sys.argv[1] == 'c':
        data = read_data(sys.argv[2])
        getcontext().prec = int(MULTIPLICATOR * min(len(data), STEP_SIZE))

        values = []
        for i in range(0, len(data), STEP_SIZE):
            to = min(i+STEP_SIZE, len(data))
            frequencies = count_frequencies(data[i:to])

            encoded_value = encode(data[i:to], frequencies)

            zip_encoded_value = decimal_to_string(encoded_value)
            values.append(Value(zip_encoded_value, frequencies, len(data[i:to])))

        save_object(values, sys.argv[3])
    else:
        loaded_values = load_object(sys.argv[2])
        getcontext().prec = int(MULTIPLICATOR * loaded_values[0].data_len)
        data = ''

        i = 0
        for loaded_value in loaded_values:
            print(i, 'out of', len(loaded_values), 'blocks done')
            i += 1
            new_encoded_value = string_to_decimal(loaded_value.encoded_value)

            data += decode(new_encoded_value, loaded_value.frequencies, loaded_value.data_len)

        write_data(data, sys.argv[3])

if __name__ == "__main__":
    main()
