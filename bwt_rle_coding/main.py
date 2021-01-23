import _pickle as pickle
import sys


BLOCK_SIZE = 5000


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

def rle(data):
    ret = ''
    lc = data[0]
    cnt = 0
    for c in data:
        if c == lc:
            cnt += 1
        else:
            ret += str(cnt) + lc
            lc = c
            cnt = 1
    ret += str(cnt) + c
    return ret

def derle(data):
    ret = ''
    cnt = 0
    for c in data:
        if c < '0' or c > '9':
            ret += c * cnt
            cnt = 0
        else:
            cnt *= 10
            cnt += ord(c) - ord('0')
    return ret

def encode(data):
    permutations = [data]
    for i in range(1, len(data)):
        permutations.append(data[i:] + data[:i])
    permutations.sort()
    column = ''
    for i in range(len(data)):
        column += permutations[i][len(data)-1]
    for i in range(len(data)):
        if data == permutations[i]:
            return rle(column), i

def decode(data, idd):
    column = derle(data)
    prefs = sorted(column)
    for i in range(1, len(column) - 1):
        for j in range(len(prefs)):
            prefs[j] = column[j] + prefs[j]
        prefs.sort()
    return prefs[idd] + column[idd]

def save_object(obj, filename):
    with open(filename, 'wb') as output:
        pickle.dump(obj, output)

def load_object(filename):
    with open(filename, 'rb') as inputt:
        return pickle.load(inputt)

class Value:
    def __init__(self, column, idd):
        self.column = column
        self.idd = idd

def main():
    if sys.argv[1] == 'c':
        data = read_data(sys.argv[2])

        values = []
        for i in range(0, len(data), BLOCK_SIZE):
            to = min(i+BLOCK_SIZE, len(data))
            column, idd = encode(data[i:to])
            value = Value(column, idd)
            values.append(value)

        save_object(values, sys.argv[3])
    else:
        loaded_values = load_object(sys.argv[2])
        data = ''

        i = 0
        for loaded_value in loaded_values:
            print(i, 'out of', len(loaded_values), 'blocks done')
            i += 1
            data += decode(loaded_value.column, loaded_value.idd)

        write_data(data, sys.argv[3])

if __name__ == "__main__":
    main()
